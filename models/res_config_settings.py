# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

DEFAULT_MAX_DRIVERS=3

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    max_drivers = fields.Integer(
        string='Maximum number of drivers',
        config_parameter='max.drivers',
        default=DEFAULT_MAX_DRIVERS
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        max_drivers = int(ICPSudo.get_param('max.drivers'))
        res.update(max_drivers=max_drivers)
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        if self.max_drivers < 0:
            raise ValidationError(
                _('The quantity of max drivers cant be lower than zero')
            )
        ICPSudo.set_param("max.drivers", self.max_drivers)
