# -*- coding: utf-8 -*-
from odoo import fields, models


class ContactWhatsappNumberWizard(models.TransientModel):
    _name = 'contact.whatsapp.number.wizard'
    _description = 'Editar número do WhatsApp de um contato'

    partner_id = fields.Many2one('res.partner', string='Contato', required=True)
    whatsapp_number = fields.Char(string='Número WhatsApp (bruto)')

    def action_save(self):
        self.ensure_one()
        self.partner_id.whatsapp_number = self.whatsapp_number
        return True
