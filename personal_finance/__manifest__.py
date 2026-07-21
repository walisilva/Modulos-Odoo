# -*- coding: utf-8 -*-
{
    'name': 'Finanças Pessoais',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Controle de despesas e receitas pessoais com importação de extrato OFX, categorização e relatórios.',
    'description': """
Finanças Pessoais
==================
Módulo simples para controle financeiro pessoal/doméstico, independente do
fluxo corporativo de despesas (hr_expense) e do app Accounting:

- Cadastro de bancos, formas de pagamento, cartões de crédito (etiqueta
  informativa com dia de vencimento) e contas com saldo calculado.
- Categorias hierárquicas (despesa / receita / neutro).
- Importação de extrato bancário em OFX, com deduplicação por FITID e
  categorização automática por regras de padrão de texto.
- Tela de categorização dos lançamentos importados sem categoria, com opção
  de salvar a categorização como regra para próximas importações.
- Relatórios analítico (lista), sintético (tabela dinâmica) e gráficos numa
  única tela.

Requer a biblioteca Python `ofxtools` (não vem instalada no Odoo por
padrão) — ver README do módulo.
    """,
    'author': 'Wali Silva',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/finance_bank_views.xml',
        'views/finance_payment_method_views.xml',
        'views/finance_card_views.xml',
        'views/finance_account_views.xml',
        'views/finance_category_views.xml',
        'views/finance_category_rule_views.xml',
        'views/finance_line_views.xml',
        'views/finance_balance_report_views.xml',
        'wizards/finance_ofx_import_wizard_views.xml',
        'wizards/finance_set_category_wizard_views.xml',
        'views/menus.xml',
    ],
    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
