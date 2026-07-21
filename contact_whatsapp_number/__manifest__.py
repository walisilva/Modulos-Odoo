# -*- coding: utf-8 -*-
{
    'name': 'Número WhatsApp do Contato',
    'version': '19.0.1.0.0',
    'category': 'Contacts',
    'summary': 'Campo com o número de WhatsApp "cru" do contato (para integrações automáticas), editável só por um grupo restrito.',
    'description': """
Número WhatsApp do Contato
============================
Adiciona um campo `whatsapp_number` em Contatos com o número de telefone
exatamente como recebido de uma integração de WhatsApp (só dígitos, com
código do país, sem formatação) — usado para casar mensagens recebidas
com o contato certo sem depender de normalizar o campo Telefone (que fica
formatado para exibição).

O campo é visível para qualquer usuário com acesso a Contatos, mas só é
editável por quem estiver no grupo "Pode editar número do WhatsApp".
    """,
    'author': 'Wali Silva',
    'license': 'LGPL-3',
    'depends': ['base', 'contacts'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'wizards/contact_whatsapp_number_wizard_views.xml',
    ],
    'images': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
