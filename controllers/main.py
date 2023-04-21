# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import json

class VehicleController(http.Controller):

    @http.route('/vehiculos/consulta/<string:secuencia>', auth='public')
    def consulta_vehiculo(self, secuencia, **kwargs):
        vehicle = request.env['vehicle'].sudo().search(
            [('sequence', '=', secuencia)], limit=1
        )
        if vehicle:
            data = {
                'seq': secuencia,
                'type': vehicle.type,
                'plate': vehicle.domain,
                'state': vehicle.state
            }
        else:
            data = {}
        json_data = json.dumps(data)
        return http.Response(json_data)
