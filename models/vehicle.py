# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime


class Vehicle(models.Model):
    _name = "vehicle"
    _rec_name = "sequence"
    _description = "Vehicles"

    sequence = fields.Char(
        string="Sequence",
        readonly=True
    )
    type = fields.Selection(
        string="Type",
        selection=[
            ('sedan', 'Sedan'),
            ('bus', 'Bus'),
            ('micro', 'Micro')
        ]
    )
    driver_id = fields.Many2one(
        string='Driver',
        comodel_name='driver'
    )
    domain = fields.Char(
        string="Domain"
    )
    active_date = fields.Datetime(
        string="Active Date",
        readonly=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('inactive', 'Inactive')
        ],
        default="draft"
    )

    @api.model
    def create(self, vals):
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code(
                'vehicle.sequence') or _('New')
        return super(Vehicle, self).create(vals)

    @api.constrains('domain')
    def _check_domain_unique(self):
        for rec in self:
            if self.search_count([('domain', '=', rec.domain)]) > 1:
                raise ValidationError(_(
                    "There already exists a vehicle whith this domain"
                ))

    @api.onchange('type')
    def onchange_vehicle_type(self):
        for rec in self:
            rec.driver_id = False

    @api.constrains('state')
    def update_active_date(self):
        for rec in self:
            if rec.state == 'active':
                rec.active_date = datetime.now()
