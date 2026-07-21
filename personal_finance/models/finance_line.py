# -*- coding: utf-8 -*-
import re

from odoo import api, fields, models


class PersonalFinanceLine(models.Model):
    _name = 'personal.finance.line'
    _description = 'Lançamento de finanças pessoais'
    _order = 'date desc, date_created desc'

    date = fields.Date(string='Data', required=True, default=fields.Date.context_today)
    description = fields.Char(string='Descrição', required=True)
    debit = fields.Float(string='Débito', digits=(16, 2))
    credit = fields.Float(string='Crédito', digits=(16, 2))
    balance = fields.Float(
        string='Saldo', digits=(16, 2), compute='_compute_balance', store=True,
    )
    date_created = fields.Datetime(
        string='Criado em', readonly=True, required=True, default=fields.Datetime.now,
    )
    source = fields.Selection(
        [('manual', 'Manual'), ('generated', 'Gerado')],
        string='Origem', readonly=True, default='manual',
    )
    state = fields.Selection(
        [('new', 'Novo'), ('ticked', 'Conciliado'), ('cancelled', 'Cancelado')],
        string='Estado', default='new',
    )
    date_effect = fields.Date(string='Data efetiva')
    place = fields.Char(string='Local')
    category_id = fields.Many2one('personal.finance.category', string='Categoria')
    account_id = fields.Many2one('personal.finance.account', string='Conta', required=True)

    @api.depends('debit', 'credit')
    def _compute_balance(self):
        for line in self:
            line.balance = line.credit - line.debit

    @api.model_create_multi
    def create(self, vals_list):
        active_categories = self.env['personal.finance.category'].search([('active', '=', True)])
        for vals in vals_list:
            if vals.get('category_id') or not vals.get('description'):
                continue
            for category in active_categories:
                if re.search(re.escape(category.name), vals['description'], re.IGNORECASE):
                    vals['category_id'] = category.id
                    break
        return super().create(vals_list)
