# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json


class HospitalController(http.Controller):

    @http.route('/pacientes/consulta/<string:secuencia>', type='http', auth='public', methods=['GET'], csrf=False)
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
            
            # Mapeo de estados
            estado_map = {
                'borrador': 'draft',
                'alta': 'alta',
                'baja': 'baja'
            }
            
            response = {
                'seq': paciente.secuencia,
                'name': paciente.nombre_apellido,
                'rnc': paciente.rnc,
                'state': estado_map.get(paciente.estado, paciente.estado)
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