{
    'name': 'Material Module',
    'version': '1.0',
    'description': 'Material Module For Test Backend Developer',
    'summary': 'Material Module For Test Backend Developer',
    'author': 'Nurfachri Daffa Alhakim',
    'license': 'LGPL-3',
    'category': 'Product',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/material_views.xml',
        'views/partner_views.xml',
    ],
    'assets': {
    },

    'auto_install': False,
    'application': True,
    'installable': True
}