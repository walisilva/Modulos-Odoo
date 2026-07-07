# -*- coding: utf-8 -*-
import re

from odoo import fields, models
from odoo.exceptions import UserError


class WhatsappSendWizard(models.TransientModel):
    _name = 'whatsapp.send.wizard'
    _description = 'Enviar mensagem de WhatsApp'

    partner_id = fields.Many2one('res.partner', string='Contato')
    instance_id = fields.Many2one(
        'evolution.instance', required=True, string='Número (instância)',
        domain=[('state', '=', 'open')],
        default=lambda self: self.env['evolution.instance'].search(
            [('state', '=', 'open')], limit=1,
        ),
    )
    phone = fields.Char(required=True, help="Número com DDI e DDD, só dígitos. Ex: 5511999999999")
    message = fields.Text(required=True)

    def action_send(self):
        self.ensure_one()
        phone = re.sub(r'\D', '', self.phone or '')
        if not phone:
            raise UserError('Informe um número de telefone válido.')

        log_vals = {
            'partner_id': self.partner_id.id,
            'instance_id': self.instance_id.id,
            'phone': phone,
            'message': self.message,
        }
        try:
            self.instance_id.send_text_message(phone, self.message)
            log_vals['state'] = 'sent'
        except UserError as exc:
            log_vals['state'] = 'error'
            log_vals['error_message'] = str(exc)
            self.env['whatsapp.message.log'].create(log_vals)
            raise

        self.env['whatsapp.message.log'].create(log_vals)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Mensagem enviada',
                'message': f'WhatsApp enviado para {phone}.',
                'type': 'success',
                'sticky': False,
            },
        }
