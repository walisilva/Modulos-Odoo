# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PersonalFinanceCategory(models.Model):
    _name = 'personal.finance.category'
    _description = 'Categoria de lançamento financeiro pessoal'
    _order = 'complete_name'
    _parent_store = True
    _parent_name = 'parent_id'
    _rec_name = 'complete_name'

    name = fields.Char(string='Categoria', required=True, translate=True)
    parent_id = fields.Many2one(
        'personal.finance.category', string='Categoria pai', index=True, ondelete='cascade',
    )
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many('personal.finance.category', 'parent_id', string='Subcategorias')
    complete_name = fields.Char(
        string='Nome completo', compute='_compute_complete_name', recursive=True, store=True,
    )
    active = fields.Boolean(
        string='Ativa', default=True,
        help='Categorias inativas ficam escondidas sem precisar excluí-las.',
    )
    line_ids = fields.One2many('personal.finance.line', 'category_id', string='Lançamentos')

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = f'{category.parent_id.complete_name} / {category.name}'
            else:
                category.complete_name = category.name

    @api.constrains('parent_id')
    def _check_parent_recursion(self):
        if not self._check_recursion():
            raise ValidationError(
                'Erro! Não é possível criar categorias recursivas (uma categoria não pode ser pai dela mesma).'
            )

    def name_search(self, name='', args=None, operator='ilike', limit=100):
        # Permite buscar pelo último segmento do nome completo (ex: buscar
        # "Mercado" encontra a categoria "Alimentação / Mercado").
        args = list(args or [])
        if name:
            short_name = name.split(' / ')[-1]
            args = [('name', operator, short_name)] + args
            categories = self.search(args, limit=limit)
            return [(category.id, category.display_name) for category in categories]
        return super().name_search(name=name, args=args, operator=operator, limit=limit)
