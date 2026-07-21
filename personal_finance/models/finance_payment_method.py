# -*- coding: utf-8 -*-
from odoo import fields, models


class PersonalFinancePaymentMethod(models.Model):
    _name = 'personal.finance.payment.method'
    _description = 'Forma de Pagamento'
    _order = 'name'

    name = fields.Char(string='Nome', required=True)
