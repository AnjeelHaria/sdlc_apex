{
    'name': 'Stock Barcode for Odoo Community Sdlc Apex custom',
    'version': '17.0',
    'category': 'Inventory',
    'summery': 'This App will add the group on Barcode menu',
    'website': 'https://www.sdlccorp.com',
    'author': 'SDLC Corp',
    'depends': ['eg_stock_barcode','sdlc_apex_custom'],
    'data': [
        'views/stock_barcode_menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': True,
}
