from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    hospital_endpoint_url = fields.Char(
        string='Endpoint Del Hospital',
        help='URL del endpoint para validación de pacientes',
        config_parameter='vertical_hospital.endpoint_url'
    )