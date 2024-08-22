# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Apex Shoes Customisation',
    'description': """
Odoo 17 Customisation for Apex Shoes

    """,
    'category': 'CRM',
    'sequence': 32,
    'author': 'SDLC Corp',
    'company': 'SDLC Corp',
    'maintainer': 'SDLC Corp',
    'website': 'https://www.sdlccorp.com',
    'depends': ['sale','stock','spreadsheet_dashboard'],
    'data': [
        'security/apex_groups.xml',
        'security/ir.model.access.csv',
        'views/res_company_view.xml',
        'views/sale_view.xml',
        'views/dashboard.xml',
        'views/product_import_wizard_views.xml',
        'views/stock_update_wiz_views.xml',
        # 'views/sales_web_page.xml',
    ],
    # "assets": {
    #     "web.assets_frontend": [
    #         "sdlc_apex_custom/static/src/js/sales_order.js",
    #         "sdlc_apex_custom/static/src/css/sales_order.css",
    #     ],
    # },
    'license': 'AGPL-3',
    'auto_install': False,
    'installable': True,
}
