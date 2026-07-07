# -*- coding: utf-8 -*-
from odoo import fields, models


class WhatsappMessageLog(models.Model):
    _name = 'whatsapp.message.log'
    _description = 'Histórico de envio de mensagens WhatsApp'
    _order = 'create_date desc'

    partner_id = fields.Many2one('res.partner', string='Contato', ondelete='set null')
    instance_id = fields.Many2one('evolution.instance', string='Instância', required=True)
    phone = fields.Char(required=True)
    message = fields.Text(required=True)
    state = fields.Selection(
        [('sent', 'Enviado'), ('error', 'Erro')], required=True, default='sent',
    )
    error_message = fields.Text()
