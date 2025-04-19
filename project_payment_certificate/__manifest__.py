{
    'name': 'Project Payment Certificate',
    'version': '1.0',
    'summary': 'Payment Certificate feature linked to Project and Delivery Note with Invoice creation',
    'category': 'Project',
    'author': 'Omid Mavluddin',
    'depends': ['project', 'stock', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_views.xml',
        'views/payment_certificate_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
