# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

{
    'name': 'Label Printing From Zebra Printer',
    'version': '17.0.1.0',
    'summary': 'An app which helps to send labels directly to the zebra label printer',
    'description': """
This module provides to print product,location and shipping label from Zebra Printer
====================================================================================

    """,
    'category': 'Printer',
    'license': 'OPL-1',
    'author': 'Kanak Infosystems LLP.',
    'website': 'https://www.kanakinfosystems.com',
    'images': ['static/description/banner.gif'],
    'depends': ['sale_stock', 'barcodes'],
    'data': [
        'security/ir.model.access.csv',
        'views/zebra_printer_view.xml',
        'views/res_company_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            ('before', 'web/static/src/webclient/actions/action_service.js', 'label_zebra_printer/static/src/js/utils.js'),
            'label_zebra_printer/static/src/js/rsvp-3.1.0.min.js',
            'label_zebra_printer/static/src/js/sha-256.min.js',
            'label_zebra_printer/static/src/js/qz-tray.js',
            'label_zebra_printer/static/src/js/jsrsasign-latest-all-min.js',
            # 'label_zebra_printer/static/src/js/qweb_action_manager.js',
        ],
    },
    'sequence': 1,
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 50,
    'currency': 'EUR',
    'live_test_url': 'https://www.youtube.com/watch?v=O8OVx2GxuGM',
}
