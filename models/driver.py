# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime


class Driver(models.Model):
    _name = "driver"
    _rec_name="complete_name"
    _description = "Drivers"

    type = fields.Selection(
        string="Type",
        selection=[
            ('sedan', 'Sedan'),
            ('bus', 'Bus'),
            ('micro', 'Micro')
        ]
    )
    enabled_type = fields.Selection(
        string="Enabled type",
        selection=[
            ("sedan", "Sedan"),
            ("bus", "Bus"),
            ("micro", "Micro")
        ]
    )
    vat = fields.Integer(
        string="Vat"
    )
    complete_name = fields.Char(
        string="Surname and names"
    )
    birthday_date = fields.Date(
        string="Birthday date"
    )
    age = fields.Char(
        string="Age",
        readonly="True",
        compute="_compute_age"
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
    def name_search(self, name, args=None, operator='ilike', limit=100):
        filter_vehicle = self.env.context.get('filter_by_vehicle', False)
        if filter_vehicle:
            if args is None:
                args = []
            vehicle_type = filter_vehicle['type']
            if not vehicle_type:
                return []
            args.append(('type', '=', vehicle_type))
            return super(Driver, self).name_search(
                name, args=args, operator=operator, limit=limit
            )

    @api.onchange('birthday_date')
    def _compute_age(self):
        current_date = datetime.now()
        for rec in self:
            if rec.birthday_date:
                birthday_date = datetime.combine(
                    rec.birthday_date, datetime.min.time()
                )
                age_difference = current_date - birthday_date
                rec.age = int(age_difference.days / 365.25)
            else:
                rec.age = False

    @api.constrains('birthday_date')
    def verify_birthday_date(self):
        for rec in self:
            if not rec.birthday_date:
                continue
            if rec.birthday_date > datetime.now().date():
                raise ValidationError(_(
                    "Driver birthday date cant be greater than current date"
                ))

    @api.model
    def create(self, vals):
        current_drivers = self.search_count([])
        ICPSudo = self.env['ir.config_parameter'].sudo()
        max_drivers = int(ICPSudo.get_param('max.drivers'))
        if current_drivers >= max_drivers and max_drivers != 0:
            raise ValidationError(_(
                "The maximum number of drivers has been exceeded"
            ))
        return super(Driver, self).create(vals)

