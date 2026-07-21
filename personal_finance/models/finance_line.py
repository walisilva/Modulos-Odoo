# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PersonalFinanceLine(models.Model):
    _name = 'personal.finance.line'
    _description = 'Lançamento de finanças pessoais'
    _order = 'date desc, id desc'

    date = fields.Date(string='Data', required=True, default=fields.Date.context_today)
    description = fields.Char(string='Descrição', required=True)
    income = fields.Float(string='Entrada', digits=(16, 2), default=0.0)
    expense = fields.Float(string='Saída', digits=(16, 2), default=0.0)
    amount = fields.Float(
        string='Valor', digits=(16, 2), compute='_compute_amount', store=True,
        help='Positivo para receita, negativo para despesa — calculado a partir de Entrada/Saída, usado nos cálculos de saldo e relatórios.',
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

    @api.depends('income', 'expense')
    def _compute_amount(self):
        for line in self:
            line.amount = line.income - line.expense

    @api.constrains('income', 'expense')
    def _check_income_expense(self):
        for line in self:
            if line.income and line.expense:
                raise ValidationError(
                    f'O lançamento "{line.description}" tem valor preenchido em Entrada e em Saída ao mesmo tempo — preencha só um dos dois.'
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('category_id') or not vals.get('description'):
                continue
            category = self.env['personal.finance.category.rule']._match(vals['description'])
            if category:
                vals['category_id'] = category.id
        return super().create(vals_list)
