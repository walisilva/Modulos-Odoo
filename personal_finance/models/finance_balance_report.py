# -*- coding: utf-8 -*-
from odoo import fields, models, tools


class PersonalFinanceBalanceReport(models.Model):
    _name = 'personal.finance.balance.report'
    _description = 'Relatório de evolução de saldo por conta'
    _auto = False
    _order = 'year asc, month asc'

    account = fields.Char(string='Conta', readonly=True)
    year = fields.Integer(string='Ano', readonly=True)
    month = fields.Integer(string='Mês', readonly=True)
    balance = fields.Float(string='Saldo', digits=(16, 2), readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT row_number() OVER (ORDER BY year, month, account) AS id, account, year, month, balance
                FROM (
                    SELECT
                        pfa.name AS account,
                        EXTRACT(year FROM pfl.date)::int AS year,
                        EXTRACT(month FROM pfl.date)::int AS month,
                        SUM(SUM(pfl.credit - pfl.debit))
                            OVER (PARTITION BY pfa.name ORDER BY EXTRACT(year FROM pfl.date)::int, EXTRACT(month FROM pfl.date)::int)
                            AS balance
                    FROM personal_finance_line pfl
                    INNER JOIN personal_finance_account pfa ON pfa.id = pfl.account_id
                    GROUP BY pfa.name, EXTRACT(year FROM pfl.date)::int, EXTRACT(month FROM pfl.date)::int
                ) grouped
            )
        """ % self._table)
