# -*- coding: utf-8 -*-
{
    "name": "Frota - Locacao BR (Fleet Leasing)",
    "version": "18.0.1.0.0",
    "category": "Fleet/Sales",
    "summary": "Gestao de locacao de veiculos (oneribus/frota) integrada com Vendas e Financeiro",
    "description": """
        Modulo white-label para locacao de frota de onibus (fretamento e turismo).
        Extende sale.order e fleet.vehicle para gerar contratos de locacao,
        travar agenda do veiculo e preparar hook para CT-e OS.
    """,
    "author": "Wali Silva",
    "website": "",
    "depends": [
        "base",
        "sale_management",
        "fleet",
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "views/fleet_vehicle_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "LGPL-3",
}
