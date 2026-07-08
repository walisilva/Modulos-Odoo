# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

"""
Herdanca do modelo sale.order (Pedido de Venda) para locacao de frota.

Adiciona vinculo com veiculo, periodo da locacao e hook para geracao
futura de CT-e OS via API (Gateway Fiscal).
"""

import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class SaleOrderFleetLeasing(models.Model):
    """Estende sale.order com dados de locacao de frota."""

    _inherit = "sale.order"

    # ----------------------------------------------------------
    # Campos especificos de locacao
    # ----------------------------------------------------------

    vehicle_id = fields.Many2one(
        comodel_name="fleet.vehicle",
        string="Veiculo / Onibus",
        ondelete="restrict",
        help="Veiculo (onibus) vinculado a este contrato de locacao.",
        index=True,
    )

    leasing_start_date = fields.Datetime(
        string="Inicio da Locacao",
        help="Data/hora de inicio do periodo de locacao.",
    )

    leasing_end_date = fields.Datetime(
        string="Fim da Locacao",
        help="Data/hora de termino do periodo de locacao.",
    )

    # ----------------------------------------------------------
    # Metodos acao
    # ----------------------------------------------------------

    def action_generate_cte_os_json(self):
        """
        Hook para Gateway Fiscal (CT-e OS).

        Ainda nao dispara requisicao HTTP externa. Apenas monta o payload
        JSON com os dados do tomador, placa do veiculo, valor e datas,
        registrando no log para auditoria.

        Retorna o dict (payload) para uso futuro na integracao.
        """
        self.ensure_one()
        partner = self.partner_id
        vehicle = self.vehicle_id

        payload = {
            "tomador": {
                "nome": partner.name,
                "documento": partner.vat or partner.cnpj_cpf or "",
                "endereco": partner.street or "",
                "cidade": partner.city or "",
                "uf": partner.state_id.code if partner.state_id else "",
                "cep": partner.zip or "",
            },
            "veiculo": {
                "placa": vehicle.license_plate or "",
                "renavam": vehicle.renavam or "",
                "chassi": vehicle.chassis_number or "",
                "marca": vehicle.model_id.brand_id.name if vehicle.model_id and vehicle.model_id.brand_id else "",
                "modelo": vehicle.model_id.name if vehicle.model_id else "",
            },
            "contrato": {
                "pedido_id": self.id,
                "numero": self.name,
                "data_emissao": str(self.date_order or ""),
                "inicio_locacao": str(self.leasing_start_date or ""),
                "fim_locacao": str(self.leasing_end_date or ""),
                "valor_total": self.amount_total,
                "valor_bruto": self.amount_untaxed,
            },
            "tipo_servico": "Locacao de Frota (Fretamento/Turismo)",
            "observacoes": self.note or "",
        }

        _logger.info("=== CT-e OS Payload (Pedido %s) ===", self.name)
        _logger.info(payload)
        _logger.info("=== Fim Payload ===")

        return payload
