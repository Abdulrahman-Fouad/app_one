{
    'name': 'App One',
    'author': 'Fo2shiria',
    'version': '17.0.0.1.0',
    'summary': 'My first App in Odoo',
    'sequence': 10,
    'description': """
      App One
====================
    """,
    'category': 'Testing',
    'depends': ['base', 'sale_management', 'account', 'mail', 'contacts'
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/sale_order_view.xml',
        'views/res_partner_view.xml',
        'views/building_view.xml',
        'reports/property_report.xml'
    ],
    'assets': {
        'web.assets_backend': ['app_one/static/src/css/property.css']
    },
    'application': True,
}
