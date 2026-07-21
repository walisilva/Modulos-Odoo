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
    category_type = fields.Selection(
        [('expense', 'Despesa'), ('income', 'Receita'), ('neutral', 'Neutro/Transferência')],
        string='Tipo', default='expense', required=True,
        help='Categorias "Neutro/Transferência" (ex: transferência entre contas próprias, estorno) '
             'ficam de fora dos totais de despesa/receita nos relatórios.',
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
