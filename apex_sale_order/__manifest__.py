# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

{
    "name": "Apex Sale Orders",
    "summary": "Allows to create and manage apex sale orders",
    'category': 'Sales/Sales',
    "version": "17.0.1.0.0",
    'author': 'SDLC Corp',
    "license": "LGPL-3",
    'website': 'https://www.sdlccorp.com',
    "depends": ["sdlc_apex_custom"],
    "data": [
        "data/ir_sequence_data.xml",
        "security/ir.model.access.csv",
        "views/apex_sale_order.xml",
        "views/stock_quant.xml",
        "views/menu.xml",
        "wizard/apex_sale_order_approve_wizard_view.xml",
    ],
    "application": True,
    "installable":True
}
