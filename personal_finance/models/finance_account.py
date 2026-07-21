# -*- coding: utf-8 -*-
import datetime
from calendar import monthrange
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class PersonalFinanceAccount(models.Model):
    _name = 'personal.finance.account'
    _description = 'Conta (banco/carteira) de finanças pessoais'
    _order = 'name asc'

    name = fields.Char(string='Nome', required=True)
    bank = fields.Char(string='Banco', required=True)
    account_type = fields.Selection(
        [('checking', 'Conta corrente'), ('savings', 'Poupança')],
        string='Tipo',
    )
    account_number = fields.Char(string='Número da conta')
    line_ids = fields.One2many('personal.finance.line', 'account_id', string='Lançamentos')

    balance = fields.Float(
        string='Saldo atual', digits=(16, 2), compute='_compute_balances',
    )
    balance_month = fields.Float(
        string='Saldo fim do mês', digits=(16, 2), compute='_compute_balances',
    )
    balance_next_month = fields.Float(
        string='Saldo fim do mês seguinte', digits=(16, 2), compute='_compute_balances',
    )
    balance_ticked = fields.Float(
        string='Saldo conciliado', digits=(16, 2), compute='_compute_balances',
    )

    @api.depends('line_ids.debit', 'line_ids.credit', 'line_ids.date', 'line_ids.state')
    def _compute_balances(self):
        today = fields.Date.context_today(self)
        month_end = today + relativedelta(day=monthrange(today.year, today.month)[1])
        next_month = today + relativedelta(months=1)
        next_month_end = next_month + relativedelta(day=monthrange(next_month.year, next_month.month)[1])

        for account in self:
            balance = 0.0
            balance_month = 0.0
            balance_next_month = 0.0
            balance_ticked = 0.0
            for line in account.line_ids:
                amount = line.credit - line.debit
                if line.date <= today:
                    balance += amount
                if line.date <= month_end:
                    balance_month += amount
                if line.date <= next_month_end:
                    balance_next_month += amount
                if line.state == 'ticked':
                    balance_ticked += amount
            account.balance = balance
            account.balance_month = balance_month
            account.balance_next_month = balance_next_month
            account.balance_ticked = balance_ticked
