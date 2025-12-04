# -*- coding: utf-8 -*-
{
    'name': 'Vertical Hospital',
    'version': '18.0.1.0.0',
    'summary': 'Sistema de gestión hospitalaria para pacientes y tratamientos',
    'description': """
        Módulo de gestión hospitalaria que incluye:
        - Gestión de pacientes
        - Gestión de tratamientos
        - Reportes en PDF
        - Web service REST
        - Auditoría de cambios
    """,
    'author': 'lfernandez',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/paciente_views.xml',
        'views/tratamiento_views.xml',
        'report/paciente_report.xml',
        'report/paciente_report_template.xml',
        'views/menu_views.xml',
    ],
    'images': ['static/description/icon.png'],
}