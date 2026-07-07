# -*- coding: utf-8 -*-
import logging

import requests

from odoo import fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 20


class EvolutionConfig(models.Model):
    _name = 'evolution.config'
    _description = 'Configuração da Evolution API'

    name = fields.Char(required=True)
    base_url = fields.Char(
        required=True,
        help="URL base da Evolution API, sem barra no final. Ex: http://192.168.0.100:8082",
    )
    api_key = fields.Char(
        required=True,
        string='API Key global',
        help="Chave global (AUTHENTICATION_API_KEY) da Evolution API, usada para criar/gerenciar instâncias.",
    )
    active = fields.Boolean(default=True)
    instance_ids = fields.One2many('evolution.instance', 'config_id', string='Instâncias')

    def _clean_base_url(self):
        self.ensure_one()
        return (self.base_url or '').rstrip('/')

    def _request(self, method, path, headers=None, instance_api_key=None, **kwargs):
        """Chamada HTTP genérica contra a Evolution API desta configuração.

        `instance_api_key`, quando informado, sobrepõe a API key global no
        header 'apikey' (algumas rotas da Evolution exigem a key da própria
        instância em vez da key global).
        """
        self.ensure_one()
        url = f"{self._clean_base_url()}{path}"
        final_headers = {
            'apikey': instance_api_key or self.api_key,
            'Content-Type': 'application/json',
        }
        if headers:
            final_headers.update(headers)
        try:
            response = requests.request(
                method, url, headers=final_headers, timeout=DEFAULT_TIMEOUT, **kwargs
            )
        except requests.exceptions.RequestException as exc:
            _logger.error('Erro ao chamar Evolution API (%s %s): %s', method, url, exc)
            raise UserError(
                f"Não foi possível conectar na Evolution API em {self._clean_base_url()}.\n"
                f"Detalhe: {exc}"
            ) from exc

        if response.status_code >= 400:
            _logger.error(
                'Evolution API retornou erro %s em %s %s: %s',
                response.status_code, method, url, response.text,
            )
            raise UserError(
                f"Evolution API retornou erro {response.status_code} em {path}:\n"
                f"{response.text[:500]}"
            )

        if not response.content:
            return {}
        try:
            return response.json()
        except ValueError:
            return {'raw': response.text}

    def action_test_connection(self):
        self.ensure_one()
        self._request('GET', '/instance/fetchInstances')
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Conexão OK',
                'message': 'A Evolution API respondeu corretamente.',
                'type': 'success',
                'sticky': False,
            },
        }
