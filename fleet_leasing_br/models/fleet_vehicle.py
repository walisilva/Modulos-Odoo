# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

"""
Herdanca do modelo fleet.vehicle para exibir status de disponibilidade
e Smart Button com contagem de locacoes.
"""

import logging
from datetime import datetime
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class FleetVehicleFleetLeasing(models.Model):
    """Estende fleet.vehicle com status de disponibilidade e stats de locacao."""

    _inherit = "fleet.vehicle"

    # ----------------------------------------------------------
    # Campos computados
    # ----------------------------------------------------------

    leasing_status = fields.Selection(
        selection=[
            ("available", "Disponivel"),
            ("leased", "Em Locacao"),
        ],
        string="Status de Locacao",
        compute="_compute_leasing_status",
        store=True,
        help="Indica se o veiculo esta disponivel ou em locacao no momento.",
    )

    leasing_order_count = fields.Integer(
        string="Total de Locacoes",
        compute="_compute_leasing_order_count",
        help="Quantidade de contratos de locacao associados a este veiculo.",
    )

    # ----------------------------------------------------------
    # Metodos compute
    # ----------------------------------------------------------

    @api.depends("vehicle_sale_order_ids", "vehicle_sale_order_ids.state",
                 "vehicle_sale_order_ids.leasing_start_date",
                 "vehicle_sale_order_ids.leasing_end_date")
    def _compute_leasing_status(self):
        """
        Computa se o onibus esta 'Disponivel' ou 'Em Locacao'.

        Logica: varre os Pedidos de Venda confirmados (sale.order) que
        apontam para este veiculo e cujo periodo (inicio/fim) engloba
        a data/hora atual.
        """
        now = datetime.now()
        for record in self:
            leased = False
            for order in record.vehicle_sale_order_ids:
                if order.state in ("sale", "done"):
                    start = order.leasing_start_date
                    end = order.leasing_end_date
                    if start and end and start <= now <= end:
                        leased = True
                        break
                    elif start and not end and start <= now:
                        # Locacao sem fim definido (aberta)
                        leased = True
                        break
            record.leasing_status = "leased" if leased else "available"

    def _compute_leasing_order_count(self):
        """
        Conta quantos Pedidos de Venda (locacoes) existem para cada veiculo.
        """
        for record in self:
            record.leasing_order_count = len(record.vehicle_sale_order_ids)

    # ----------------------------------------------------------
    # Relacao inversa (Many2many / One2many virtual)
    # NOTA: Como herdamos sale.order com vehicle_id (Many2one),
    # o Odoo cria automaticamente o campo inverso.
    # Mas para evitar ambuiguidade, definimos explicitamente:
    # ----------------------------------------------------------

    vehicle_sale_order_ids = fields.One2many(
        comodel_name="sale.order",
        inverse_name="vehicle_id",
        string="Contratos de Locacao",
        help="Pedidos de Venda (contratos) vinculados a este veiculo.",
    )
