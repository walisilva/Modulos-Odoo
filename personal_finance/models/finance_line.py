# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PersonalFinanceLine(models.Model):
    _name = 'personal.finance.line'
    _description = 'Lançamento de finanças pessoais'
    _order = 'date desc, id desc'

    date = fields.Date(string='Data', required=True, default=fields.Date.context_today)
    description = fields.Char(string='Descrição', required=True)
    amount = fields.Float(
        string='Valor', digits=(16, 2), required=True,
        help='Positivo para receita, negativo para despesa.',
    )
    account_id = fields.Many2one('personal.finance.account', string='Conta', required=True)
    category_id = fields.Many2one('personal.finance.category', string='Categoria')
    card_id = fields.Many2one('personal.finance.card', string='Cartão')
    payment_method_id = fields.Many2one('personal.finance.payment.method', string='Forma de pagamento')
    place = fields.Char(string='Local')
    state = fields.Selection(
        [('new', 'Novo'), ('reconciled', 'Conciliado'), ('cancelled', 'Cancelado')],
        string='Estado', default='new',
    )
    source = fields.Selection(
        [('manual', 'Manual'), ('ofx', 'Importado (OFX)')],
        string='Origem', default='manual', readonly=True,
    )
    ofx_fitid = fields.Char(string='ID da transação (OFX)', readonly=True, copy=False)

    _sql_constraints = [
        (
            'ofx_fitid_account_uniq',
            'unique(account_id, ofx_fitid)',
            'Este lançamento já foi importado antes para esta conta (FITID duplicado).',
        ),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('category_id') or not vals.get('description'):
                continue
            category = self.env['personal.finance.category.rule']._match(vals['description'])
            if category:
                vals['category_id'] = category.id
        return super().create(vals_list)
