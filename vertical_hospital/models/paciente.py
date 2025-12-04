# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Paciente(models.Model):
    _name = 'hospital.paciente'
    _description = 'Paciente del Hospital'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'nombre_apellido'

    secuencia = fields.Char(
        string='Secuencia',
        required=True,
        readonly=True,
        copy=False,
        default='Nuevo'
    )
    
    nombre_apellido = fields.Char(
        string='Nombre y Apellido',
        required=True,
        tracking=True
    )
    
    rnc = fields.Char(
        string='RNC',
        required=True,
        tracking=True
    )
    
    tratamiento_ids = fields.Many2many(
        'hospital.tratamiento',
        string='Tratamientos Realizados',
        help='Tratamientos asociados al paciente'
    )
    
    fecha_hora_alta = fields.Datetime(
        string='Fecha Hora de Alta',
        default=fields.Datetime.now,
        tracking=True
    )
    
    fecha_hora_actualizacion = fields.Datetime(
        string='Fecha Hora de Actualización',
        readonly=True,
        tracking=True
    )
    
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('alta', 'Alta'),
        ('baja', 'Baja')
    ], string='Estado', default='borrador', required=True, tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('secuencia', 'Nuevo') == 'Nuevo':
            vals['secuencia'] = self.env['ir.sequence'].next_by_code('hospital.paciente') or 'Nuevo'
        vals['fecha_hora_actualizacion'] = fields.Datetime.now()
        return super(Paciente, self).create(vals)

    def write(self, vals):
        vals['fecha_hora_actualizacion'] = fields.Datetime.now()
        
        if 'rnc' in vals:
            for record in self:
                old_rnc = record.rnc
                new_rnc = vals['rnc']
                if old_rnc != new_rnc:
                    mensaje = f"RNC cambiado de '{old_rnc}' a '{new_rnc}' por {self.env.user.name}"
                    record.message_post(body=mensaje)
        
        # Auditoría para cambios en Estado
        if 'estado' in vals:
            for record in self:
                old_estado = dict(record._fields['estado'].selection).get(record.estado)
                new_estado = dict(record._fields['estado'].selection).get(vals['estado'])
                if old_estado != new_estado:
                    mensaje = f"Estado cambiado de '{old_estado}' a '{new_estado}' por {self.env.user.name}"
                    record.message_post(body=mensaje)
        
        return super(Paciente, self).write(vals)

    @api.constrains('rnc')
    def _check_rnc(self):
        for record in self:
            if record.rnc and not record.rnc.isdigit():
                raise ValidationError('El RNC no debe contener letras, solo números.')
            
            if record.rnc and len(rnc) > 11 or len(rnc) < 9:
                raise ValidationError('El rnc del usuario debe de ser mayor a 8 digitos y menor a 11 digitos')

    def action_set_borrador(self):
        self.write({'estado': 'borrador'})

    def action_set_alta(self):
        self.write({'estado': 'alta'})

    def action_set_baja(self):
        self.write({'estado': 'baja'})