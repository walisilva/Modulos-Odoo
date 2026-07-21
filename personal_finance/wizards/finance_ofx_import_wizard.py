# -*- coding: utf-8 -*-
import base64
import io

from odoo import fields, models
from odoo.exceptions import UserError


class PersonalFinanceOfxImportWizard(models.TransientModel):
    _name = 'personal.finance.ofx.import.wizard'
    _description = 'Importar extrato OFX'

    import_file = fields.Binary(string='Arquivo OFX', required=True)
    import_filename = fields.Char(string='Nome do arquivo')
    account_id = fields.Many2one('personal.finance.account', string='Conta', required=True)
    state = fields.Selection([('choose', 'Escolher'), ('done', 'Concluído')], default='choose')
    message = fields.Text(string='Resultado', readonly=True)
    generated_line_ids = fields.Many2many('personal.finance.line', string='Lançamentos importados', readonly=True)

    def action_import(self):
        self.ensure_one()
        from ofxtools.Parser import OFXTree

        raw = base64.b64decode(self.import_file)
        tree = OFXTree()
        try:
            tree.parse(io.BytesIO(raw))
            ofx = tree.convert()
        except Exception as exc:
            raise UserError(f'Não foi possível ler o arquivo OFX: {exc}') from exc

        if not ofx.statements:
            raise UserError('Nenhum extrato encontrado dentro do arquivo OFX.')
        if len(ofx.statements) > 1:
            raise UserError(
                'Este arquivo tem mais de um extrato dentro (mais de uma conta). '
                'Exporte cada conta em um arquivo OFX separado e importe um de cada vez.'
            )
        stmt = ofx.statements[0]

        account = self.account_id
        acct_info = getattr(stmt, 'account', None)
        if acct_info and account.ofx_bankid and account.ofx_acctid:
            file_bankid = getattr(acct_info, 'bankid', None)
            file_acctid = getattr(acct_info, 'acctid', None)
            if file_bankid and file_acctid and (file_bankid != account.ofx_bankid or file_acctid != account.ofx_acctid):
                raise UserError(
                    f'O arquivo indica banco/conta {file_bankid}/{file_acctid}, mas a conta '
                    f'selecionada ("{account.name}") está cadastrada com {account.ofx_bankid}/'
                    f'{account.ofx_acctid}. Confira se escolheu a conta certa.'
                )

        existing_fitids = set(
            self.env['personal.finance.line'].search([
                ('account_id', '=', account.id), ('ofx_fitid', '!=', False),
            ]).mapped('ofx_fitid')
        )

        vals_list = []
        skipped = 0
        for txn in stmt.transactions:
            fitid = txn.fitid
            if fitid and fitid in existing_fitids:
                skipped += 1
                continue
            trnamt = float(txn.trnamt)
            vals_list.append({
                'date': txn.dtposted.date(),
                'description': (txn.memo or txn.name or '').strip() or 'Sem descrição',
                'income': trnamt if trnamt > 0 else 0.0,
                'expense': -trnamt if trnamt < 0 else 0.0,
                'account_id': account.id,
                'source': 'ofx',
                'ofx_fitid': fitid,
            })

        lines = self.env['personal.finance.line'].create(vals_list) if vals_list else self.env['personal.finance.line']
        categorized = lines.filtered('category_id')

        self.generated_line_ids = lines
        self.state = 'done'
        self.message = (
            f'{len(lines)} lançamento(s) importado(s), {skipped} já existia(m) (ignorado(s)), '
            f'{len(categorized)} categorizado(s) automaticamente, '
            f'{len(lines) - len(categorized)} sem categoria.'
        )

        return {
            'name': 'Importar Extrato OFX',
            'type': 'ir.actions.act_window',
            'res_model': 'personal.finance.ofx.import.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def action_view_uncategorized(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id(
            'personal_finance.action_personal_finance_lines_uncategorized'
        )
        action['domain'] = [('id', 'in', self.generated_line_ids.filtered(lambda l: not l.category_id).ids)]
        return action
