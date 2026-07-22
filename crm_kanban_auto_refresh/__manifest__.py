# -*- coding: utf-8 -*-
{
    'name': 'CRM Kanban - Atualização Automática',
    'version': '19.0.1.0.0',
    'category': 'Sales/CRM',
    'summary': 'Opção de atualizar a tela do Pipeline do CRM automaticamente a cada 30 segundos.',
    'description': """
CRM Kanban - Atualização Automática
=====================================
Adiciona uma marcação (checkbox) na tela do Pipeline do CRM (view Kanban de
oportunidades) que, quando ativada, recarrega os dados da tela a cada 30
segundos, sem precisar apertar F5. Desmarcada por padrão. O recarregamento
é só dos dados (mesma chamada usada pelo botão de refresh nativo do Odoo),
não a página inteira, então a marcação não se perde entre os ciclos.
    """,
    'author': 'Wali Silva',
    'license': 'LGPL-3',
    'depends': ['crm'],
    'assets': {
        'web.assets_backend': [
            'crm_kanban_auto_refresh/static/src/crm_kanban_auto_refresh.js',
            'crm_kanban_auto_refresh/static/src/crm_kanban_auto_refresh.xml',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
