# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Tratamiento(models.Model):
    _name = 'hospital.tratamiento'
    _description = 'Tratamiento Hospitalario'
    _rec_name = 'nombre_tratamiento'

    _sql_constraints = [
        ('codigo_tratamiento_unique', 'unique(codigo_tratamiento)', 
         'El código de tratamiento debe ser único.')
    ]
    
    codigo_tratamiento = fields.Char(
        string='Código de Tratamiento',
        required=True
    )
    
    nombre_tratamiento = fields.Char(
        string='Nombre del Tratamiento',
        required=True
    )
    
    medico_tratante = fields.Char(
        string='Médico Tratante',
        required=True
    )
    
    paciente_ids = fields.Many2many(
        'hospital.paciente',
        string='Pacientes'
    )

    @api.constrains('codigo_tratamiento')
    def _check_codigo_tratamiento(self):
        for record in self:
            if record.codigo_tratamiento and '026' in record.codigo_tratamiento:
                raise ValidationError('El código de tratamiento no debe contener la secuencia "026".')
