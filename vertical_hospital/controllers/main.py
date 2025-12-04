# -*- coding: utf-8 -*-
from odoo.http import request, Controller, route
import json


class HospitalController(Controller):

    @route('/pacientes/consulta/<string:secuencia>', type='http', auth='public', methods=['GET'], csrf=False)
    def consulta_paciente(self, secuencia, **kwargs):
        """
        Endpoint REST para consultar un paciente por su secuencia
        Ejemplo: http://localhost:8069/pacientes/consulta/PA000001
        """
        try:
            paciente = request.env['hospital.paciente'].sudo().search([
                ('secuencia', '=', secuencia)
            ], limit=1)
            
            if not paciente:
                response = {
                    'error': 'Paciente no encontrado',
                    'secuencia': secuencia
                }
                return request.make_response(
                    json.dumps(response, ensure_ascii=False),
                    headers=[('Content-Type', 'application/json')],
                    status=404
                )
            
            response = {
                'seq': paciente.secuencia,
                'name': paciente.nombre_apellido,
                'rnc': paciente.rnc,
                'state': paciente.estado or "draft"
            }
            
            return request.make_response(
                json.dumps(response, ensure_ascii=False),
                headers=[('Content-Type', 'application/json')],
                status=200
            )
            
        except Exception as e:
            response = {
                'error': str(e)
            }
            return request.make_response(
                json.dumps(response, ensure_ascii=False),
                headers=[('Content-Type', 'application/json')],
                status=500
            )