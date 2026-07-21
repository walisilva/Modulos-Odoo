# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PersonalFinanceCard(models.Model):
    _name = 'personal.finance.card'
    _description = 'Cartão de Crédito'
    _order = 'name'

    name = fields.Char(string='Nome', required=True, help='Ex: "Nubank Crédito", "Itaú Platinum".')
    bank_id = fields.Many2one('personal.finance.bank', string='Banco')
    due_day = fields.Integer(string='Dia de vencimento', help='Dia do mês em que a fatura vence (1 a 31), só informativo.')

    @api.constrains('due_day')
    def _check_due_day(self):
        for card in self:
            if card.due_day and not (1 <= card.due_day <= 31):
                raise ValidationError('O dia de vencimento deve estar entre 1 e 31.')
