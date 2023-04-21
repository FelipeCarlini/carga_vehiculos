# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class VehicleChargeConfig(models.Model):
    _name = "vehicle.charge.config"
    _description = "Vehicle and driver configuration"

    max_drivers = fields.Integer(
        string="Maximum number of drivers",
        readonly=True
    )
