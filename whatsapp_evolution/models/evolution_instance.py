# -*- coding: utf-8 -*-
import logging

from odoo import fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class EvolutionInstance(models.Model):
    _name = 'evolution.instance'
    _description = 'Instância (número) de WhatsApp na Evolution API'
    _rec_name = 'name'

    name = fields.Char(
        required=True,
        help="Nome da instância na Evolution API (sem espaços/acentos, ex: odoo-vendas).",
    )
    config_id = fields.Many2one(
        'evolution.config', required=True, ondelete='cascade', string='Configuração',
    )
    instance_api_key = fields.Char(
        string='API Key da instância',
        help="Preenchida automaticamente pela Evolution API ao criar a instância.",
    )
    state = fields.Selection(
        [
            ('draft', 'Não criada'),
            ('connecting', 'Aguardando leitura do QR Code'),
            ('open', 'Conectado'),
            ('closed', 'Desconectado'),
        ],
        default='draft',
        required=True,
    )
    qrcode_image = fields.Binary(string='QR Code')
    phone_number = fields.Char(string='Número conectado')
    last_checked = fields.Datetime(string='Última verificação')
    active = fields.Boolean(default=True)

    def _extract_qrcode_b64(self, data):
        """Tenta extrair o base64 do QR Code de diferentes formatos de resposta
        usados pela Evolution API conforme a versão."""
        qrcode = data.get('qrcode') or data
        b64 = None
        if isinstance(qrcode, dict):
            b64 = qrcode.get('base64') or qrcode.get('code')
        elif isinstance(qrcode, str):
            b64 = qrcode
        if not b64:
            return False
        if b64.startswith('data:image'):
            b64 = b64.split(',', 1)[-1]
        return b64

    def action_create_instance(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError('Esta instância já foi criada na Evolution API.')

        payload = {
            'instanceName': self.name,
            'qrcode': True,
            'integration': 'WHATSAPP-BAILEYS',
        }
        result = self.config_id._request('POST', '/instance/create', json=payload)

        instance_key = False
        hash_data = result.get('hash')
        if isinstance(hash_data, dict):
            instance_key = hash_data.get('apikey')
        elif isinstance(hash_data, str):
            instance_key = hash_data

        vals = {'state': 'connecting', 'last_checked': fields.Datetime.now()}
        if instance_key:
            vals['instance_api_key'] = instance_key

        qrcode_b64 = self._extract_qrcode_b64(result)
        if qrcode_b64:
            vals['qrcode_image'] = qrcode_b64

        self.write(vals)

        if not qrcode_b64:
            # Algumas versões só devolvem o QR Code pela rota /instance/connect
            self.action_refresh_qrcode()

        return self._reload_action()

    def action_refresh_qrcode(self):
        self.ensure_one()
        result = self.config_id._request(
            'GET', f'/instance/connect/{self.name}', instance_api_key=self.instance_api_key,
        )
        qrcode_b64 = self._extract_qrcode_b64(result)
        vals = {'last_checked': fields.Datetime.now()}
        if qrcode_b64:
            vals['qrcode_image'] = qrcode_b64
            vals['state'] = 'connecting'
        self.write(vals)
        return self._reload_action()

    def action_check_status(self):
        self.ensure_one()
        result = self.config_id._request(
            'GET', f'/instance/connectionState/{self.name}', instance_api_key=self.instance_api_key,
        )
        instance_data = result.get('instance', result)
        raw_state = (instance_data.get('state') or '').lower()
        state_map = {
            'open': 'open',
            'connected': 'open',
            'connecting': 'connecting',
            'close': 'closed',
            'closed': 'closed',
        }
        vals = {'last_checked': fields.Datetime.now()}
        if raw_state in state_map:
            vals['state'] = state_map[raw_state]
            if state_map[raw_state] == 'open':
                vals['qrcode_image'] = False
        self.write(vals)
        return self._reload_action()

    def action_disconnect(self):
        self.ensure_one()
        self.config_id._request(
            'DELETE', f'/instance/logout/{self.name}', instance_api_key=self.instance_api_key,
        )
        self.write({'state': 'closed', 'qrcode_image': False, 'last_checked': fields.Datetime.now()})
        return self._reload_action()

    def action_delete_instance(self):
        self.ensure_one()
        self.config_id._request(
            'DELETE', f'/instance/delete/{self.name}', instance_api_key=self.instance_api_key,
        )
        self.write({
            'state': 'draft',
            'qrcode_image': False,
            'instance_api_key': False,
            'phone_number': False,
            'last_checked': fields.Datetime.now(),
        })
        return self._reload_action()

    def _reload_action(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def send_text_message(self, phone, message):
        """Envia uma mensagem de texto para `phone` (formato internacional,
        só dígitos, ex: 5511999999999) usando esta instância."""
        self.ensure_one()
        if self.state != 'open':
            raise UserError(
                f"A instância '{self.name}' não está conectada (status atual: {self.state})."
            )
        payload = {'number': phone, 'text': message}
        return self.config_id._request(
            'POST', f'/message/sendText/{self.name}', instance_api_key=self.instance_api_key,
            json=payload,
        )
