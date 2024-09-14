{
    'name': 'Stock Barcode for Odoo Community',
    'version': '17.0',
    'category': 'Inventory',
    'summery': 'This App will add the Barcode scanning functionality to Odoo community for version V17',
    'website': 'https://www.inkerp.com',
    'author': 'INKERP',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/stock_barcode_client_view.xml',
        'views/stock_barcode_menu.xml',
        'views/stock_picking_view.xml',
        'views/stock_picking_type_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'eg_stock_barcode/static/src/xml/stock_barcode_view.xml',
            'eg_stock_barcode/static/src/xml/delivery_order_product.xml',
            'eg_stock_barcode/static/src/xml/BarcodeStockMoveLine.xml',
            'eg_stock_barcode/static/src/xml/StockBodyFooter.xml',
            'eg_stock_barcode/static/src/js/stock_picking_handler.js',
            'eg_stock_barcode/static/src/js/delivery_order_details.js',
            'eg_stock_barcode/static/src/js/stock_barcode_scan.js',

            'eg_stock_barcode/static/src/scss/stock_barcode_scan.scss',
            'eg_stock_barcode/static/src/scss/stock_delivery_details.scss',
            'eg_stock_barcode/static/src/scss/stock_barcode_updated.css',

            'eg_stock_barcode/static/src/lib/selectize.min.js',
            'eg_stock_barcode/static/src/lib/sweetalert.min.js',
            'eg_stock_barcode/static/src/lib/selectize.css',
            'eg_stock_barcode/static/src/lib/sweetalert.css'
        ],
    },
    'images': ['static/description/banner.gif'],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': '199',
    'currency': 'EUR',
}
