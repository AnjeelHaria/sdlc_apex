from odoo import http
from odoo.http import request


class SalesOrderController(http.Controller):

    @http.route('/create_sales_order', type='http', auth='user', website=True)
    def create_sales_order_form(self, **kw):
        customers = request.env['res.partner'].search([('customer_rank', '>', 0)])
        return request.render('sdlc_apex_custom.create_sales_order_template', {
            'customers': customers,
        })

    @http.route('/submit_sales_order', type='http', auth='user', website=True, methods=['POST'])
    def submit_sales_order(self, **post):
        customer_id = int(post.get('customer_id'))
        order_lines = post.get('order_lines')

        order_lines_data = []
        for line in order_lines:
            product_id, quantity = line.split(',')
            order_lines_data.append((0, 0, {
                'product_id': int(product_id),
                'product_uom_qty': float(quantity),
            }))

        sales_order = request.env['sale.order'].create({
            'partner_id': customer_id,
            'order_line': order_lines_data,
        })

        return request.redirect('/order_confirmation')

    @http.route('/search_products', type='json', auth='user', website=True)
    def search_products(self, **post):
        search_term = post.get('search_term', '')
        products = request.env['product.product'].search([('name', 'ilike', search_term)], limit=10)
        return [{'id': product.id, 'name': product.name} for product in products]