# -*- coding: utf-8 -*-
import base64
import csv
import io

from odoo import fields, models


def _parse_amount(value):
    value = (value or '').strip().replace(',', '.')
    return float(value) if value else 0.0


class PersonalFinanceImportWizard(models.TransientModel):
    _name = 'personal.finance.import.wizard'
    _description = 'Importar lançamentos de finanças pessoais'

    import_file = fields.Binary(string='Arquivo CSV', required=True)
    import_filename = fields.Char(string='Nome do arquivo')
    account_id = fields.Many2one('personal.finance.account', string='Conta', required=True)
    message = fields.Text(string='Mensagem', readonly=True)
    state = fields.Selection(
        [('choose', 'Escolher'), ('error', 'Erro'), ('success', 'Sucesso')],
        default='choose',
    )
    generated_line_ids = fields.Many2many('personal.finance.line', string='Lançamentos gerados', readonly=True)

    def action_import(self):
        self.ensure_one()
        raw = base64.b64decode(self.import_file).decode('utf-8-sig', errors='replace')
        reader = csv.reader(io.StringIO(raw), delimiter=';')

        errors = []
        vals_list = []
        for index, row in enumerate(reader, start=1):
            if not row or not any(cell.strip() for cell in row):
                continue
            if len(row) < 6:
                errors.append(f'Linha {index}: esperado 6 colunas (data;descrição;referência;conciliado;débito;crédito), encontrado {len(row)}.')
                continue
            try:
                vals_list.append({
                    'date': row[0].strip(),
                    'description': row[1].strip(),
                    'state': 'ticked' if row[3].strip() else 'new',
                    'debit': _parse_amount(row[4]),
                    'credit': _parse_amount(row[5]),
                    'account_id': self.account_id.id,
                    'source': 'generated',
                })
            except (ValueError, IndexError) as exc:
                errors.append(f'Linha {index}: {exc}')

        if errors:
            self.state = 'error'
            self.message = '\n'.join(errors)
        else:
            lines = self.env['personal.finance.line'].create(vals_list)
            self.generated_line_ids = lines
            self.state = 'success'
            self.message = f'{len(lines)} lançamento(s) criado(s) com sucesso.'

        return {
            'name': 'Importar Lançamentos',
            'type': 'ir.actions.act_window',
            'res_model': 'personal.finance.import.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def action_view_lines(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id('personal_finance.action_personal_finance_lines_all')
        action['domain'] = [('id', 'in', self.generated_line_ids.ids)]
        return action
