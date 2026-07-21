# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PersonalFinanceSetCategoryWizard(models.TransientModel):
    _name = 'personal.finance.set.category.wizard'
    _description = 'Aplicar categoria a lançamentos'

    category_id = fields.Many2one('personal.finance.category', string='Categoria', required=True)
    rule_pattern = fields.Char(
        string='Salvar como regra (padrão)',
        help='Se preenchido, cria (ou atualiza) uma regra de categorização automática com este '
             'padrão de texto, para que a próxima importação de OFX já aplique esta categoria '
             'sozinha em lançamentos parecidos. Deixe em branco para só categorizar sem criar regra.',
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_ids = self.env.context.get('active_ids') or []
        if 'rule_pattern' in fields_list and len(active_ids) == 1:
            line = self.env['personal.finance.line'].browse(active_ids[0])
            res['rule_pattern'] = line.description
        return res

    def action_set_category(self):
        self.ensure_one()
        active_ids = self.env.context.get('active_ids', [])
        lines = self.env['personal.finance.line'].browse(active_ids)
        vals = {'category_id': self.category_id.id}
        if self.rule_pattern:
            self.env['personal.finance.category.rule']._upsert(self.rule_pattern, self.category_id.id)
            vals['has_pattern'] = True
        lines.write(vals)
        return True
