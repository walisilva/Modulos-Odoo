# -*- coding: utf-8 -*-
from odoo import fields, models


class PersonalFinanceSetCategoryWizard(models.TransientModel):
    _name = 'personal.finance.set.category.wizard'
    _description = 'Aplicar categoria a vários lançamentos'

    category_id = fields.Many2one('personal.finance.category', string='Categoria', required=True)

    def action_set_category(self):
        self.ensure_one()
        active_ids = self.env.context.get('active_ids', [])
        self.env['personal.finance.line'].browse(active_ids).write({'category_id': self.category_id.id})
