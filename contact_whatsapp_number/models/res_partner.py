# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    whatsapp_number = fields.Char(
        string='Número WhatsApp (bruto)',
        help='Número de telefone exatamente como recebido de uma integração de WhatsApp '
             '(só dígitos, com código do país, ex: 5583991065820), usado para casar mensagens '
             'recebidas com este contato automaticamente. Editar só se souber o que está fazendo — '
             'mudar ou apagar este valor quebra o casamento automático para este contato.',
        readonly=True,
    )

    def action_open_whatsapp_number_wizard(self):
        self.ensure_one()
        return {
            'name': 'Editar número do WhatsApp',
            'type': 'ir.actions.act_window',
            'res_model': 'contact.whatsapp.number.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_partner_id': self.id,
                'default_whatsapp_number': self.whatsapp_number,
            },
        }
