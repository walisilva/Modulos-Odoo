# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PersonalFinanceCategoryRule(models.Model):
    _name = 'personal.finance.category.rule'
    _description = 'Regra de categorização automática'
    _order = 'pattern'

    pattern = fields.Char(
        string='Padrão', required=True,
        help='Trecho de texto (sem diferenciar maiúsculas/minúsculas) procurado na descrição '
             'do lançamento. Se mais de uma regra combinar, vence o padrão mais longo.',
    )
    category_id = fields.Many2one('personal.finance.category', string='Categoria', required=True)
    active = fields.Boolean(string='Ativa', default=True)

    @api.model
    def _match(self, description):
        """Retorna a personal.finance.category cujo padrão mais específico
        (mais longo) aparece em `description`, ou um recordset vazio."""
        if not description:
            return self.env['personal.finance.category']
        desc_upper = description.upper()
        rules = self.search([('active', '=', True)])
        matches = rules.filtered(lambda r: r.pattern.upper() in desc_upper)
        if not matches:
            return self.env['personal.finance.category']
        best = max(matches, key=lambda r: len(r.pattern))
        return best.category_id

    @api.model
    def _upsert(self, pattern, category_id):
        """Cria uma regra nova com esse padrão, ou atualiza a categoria de uma já existente
        com o mesmo padrão exato (case-sensitive na chave, igual à ferramenta de origem)."""
        existing = self.search([('pattern', '=', pattern)], limit=1)
        if existing:
            existing.category_id = category_id
            return existing
        return self.create({'pattern': pattern, 'category_id': category_id})
