# -*- coding: utf-8 -*-
{
    'name': 'Finanças Pessoais',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Controle simples de despesas e receitas pessoais, com categorias, contas e relatórios.',
    'description': """
Finanças Pessoais
==================
Módulo simples para controle financeiro pessoal/doméstico, independente do
fluxo corporativo de despesas (hr_expense):

- Cadastro de contas (banco, carteira) com saldo atual, saldo no fim do mês
  atual/seguinte e saldo conciliado.
- Lançamentos de débito/crédito com categorias hierárquicas, atribuição
  automática de categoria por palavra-chave na descrição.
- Conciliação simples por estado (Novo / Conciliado / Cancelado).
- Relatórios em tabela dinâmica: lançamentos por categoria/conta/mês e
  evolução do saldo por conta.
- Importação de lançamentos em lote via arquivo CSV.

Portado para Odoo 19 a partir do módulo original "odoo-personal-finances"
(Odoo 8, Nicolas Raynaud, LGPL-3): https://github.com/nicoraynaud/odoo-personal-finances
    """,
    'author': 'Wali Silva',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/finance_account_views.xml',
        'views/finance_category_views.xml',
        'views/finance_line_views.xml',
        'views/finance_balance_report_views.xml',
        'wizards/finance_import_wizard_views.xml',
        'wizards/finance_set_category_wizard_views.xml',
        'views/menus.xml',
    ],
    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
