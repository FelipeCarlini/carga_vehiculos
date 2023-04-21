# -*- coding: utf-8 -*-

{
    "name": "Carga de vehículos",
    "category": "others",
    "version": "12.0.1.0.0",
    "author": "Felipe Carlini",
    "license": "AGPL-3",
    "description": "Aplicación para cargar vehículos",
    "depends": [
        "base",
        "base_setup"
    ],
    "data": [
        "views/driver.xml",
        "views/vehicle.xml",
        "views/res_config_settings_view.xml",
        "views/menuitems.xml",
        "data/vehicle_sequence.xml",
        "reports/vehicle_report.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "application": True,
}
