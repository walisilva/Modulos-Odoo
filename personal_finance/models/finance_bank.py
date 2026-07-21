# -*- coding: utf-8 -*-
from odoo import fields, models


class PersonalFinanceBank(models.Model):
    _name = 'personal.finance.bank'
    _description = 'Banco'
    _order = 'name'

    name = fields.Char(string='Nome', required=True)
    code = fields.Char(string='Código (BANKID/ISPB)', help='Código do banco, ex: BANKID do OFX (0341 para Itaú).')
