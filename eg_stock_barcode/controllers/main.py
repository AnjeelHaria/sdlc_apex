from odoo import http
from odoo.http import request


class StockPickingOperations(http.Controller):
    @http.route('/stock_details/open_picking_barcode', type='json', auth="public", website=True)
    def open_picking(self, barcode, **kwargs):
        """
        When Scanned barcode or Manually add barcode after show a location, operation types and picking order
        """
        # check stock location
        stock_location_id = request.env['stock.location'].search([('name', '=', barcode)])
        if stock_location_id:
            action = request.env.ref('stock.action_location_form').read()[0]
            form_view = [(request.env.ref('stock.view_location_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if
                                               view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = stock_location_id.id

            return_dict = {
                'action': action,
                'barcode': barcode,
                'location_id': stock_location_id.id,
                'message': 'Record found. (barcode_scan_main_event)',
            }
            return return_dict
        # check operation type
        stock_picking_type_id = request.env['stock.picking.type'].search([('name', '=', barcode)], limit=1)
        if stock_picking_type_id:
            action = stock_picking_type_id.get_stock_picking_action_picking_type_kanban()
            return_dict = {
                'action': action,
                'barcode': barcode,
                'stock_operation_type_id': stock_picking_type_id.id,
                'message': 'Record found. (barcode_scan_main_event)',
            }
            return return_dict
        # check stock picking order
        stock_picking_id = request.env['stock.picking'].search(
            [('name', '=', barcode), ('company_id', '=', request.env.company.id)])
        if stock_picking_id:
            action = request.env.ref('eg_stock_barcode.stock_picking_details_client_action').read()[0]
            params = {
                'model': 'stock.picking',
                'picking_id': stock_picking_id.id,
                'nomenclature_id': [request.env.company.nomenclature_id.id],
            }
            action = dict(action, target='fullscreen', params=params)
            action['context'] = {'active_id': stock_picking_id.id,'active_model':'stock.picking'}

            # action = {'action': action}
            return action
        else:
            return_dict = {
                'message': 'No found scanned barcode: {}'.format(barcode),
                'barcode': barcode,
            }
            return return_dict

    @http.route('/stock_details/plus_one', type='json', auth="public", website=True)
    def increase_done_quantity(self, line_id, **kwargs):
        """
        +1 stock move line done quantity
        """
        stock_move_line_id = request.env['stock.move.line'].search([('id', '=', line_id)])
        picking_id = request.env['stock.picking'].search(
            [('name', '=', stock_move_line_id.picking_id.name), ('company_id', '=', request.env.company.id)])
        if picking_id.state in ['waiting', 'confirmed', 'assigned']:
            done_quantity = stock_move_line_id.quantity + 1
            stock_move_line_id.write({
                'quantity': done_quantity,
            })
            return stock_move_line_id.quantity
        else:
            return {
                'message': 'Record can be updated only if state is in Ready or Waiting state.'
            }

    @http.route('/stock_details/decrease_one', type='json', auth="public", website=True)
    def decrease_done_quantity(self, line_id, **kwargs):
        """
        -1 stock move line done quantity
        """

        stock_move_line_id = request.env['stock.move.line'].search([('id', '=', line_id)])
        picking_id = request.env['stock.picking'].search(
            [('name', '=', stock_move_line_id.picking_id.name), ('company_id', '=', request.env.company.id)])
        if picking_id.state in ['waiting', 'confirmed', 'assigned']:
            done_quantity = stock_move_line_id.quantity - 1
            stock_move_line_id.write({
                'quantity': done_quantity,
            })
            return stock_move_line_id.quantity
        else:
            return {
                'message': 'Record can be updated only if state is in Ready or Waiting state.'
            }
