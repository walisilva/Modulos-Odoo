# -*- coding: utf-8 -*-
{
    'name': 'WhatsApp via Evolution API',
    'version': '19.0.1.0.0',
    'category': 'Discuss',
    'summary': 'Configura a Evolution API, gerencia números/instâncias de WhatsApp e envia mensagens para contatos direto do Odoo.',
    'description': """
WhatsApp via Evolution API
===========================
Integração com a Evolution API (https://github.com/EvolutionAPI/evolution-api) para:

- Configurar a URL e a API Key da Evolution API direto pelo Odoo.
- Criar e conectar números de WhatsApp (instâncias), com QR Code exibido na tela.
- Enviar mensagens de WhatsApp para contatos com um botão, com histórico de envio.
    """,
    'author': 'Wali Silva',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/evolution_config_data.xml',
        'views/evolution_config_views.xml',
        'views/evolution_instance_views.xml',
        'views/whatsapp_message_log_views.xml',
        'views/res_partner_views.xml',
        'wizards/whatsapp_send_wizard_views.xml',
        'views/menus.xml',
    ],
    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
