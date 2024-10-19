from docutils.nodes import pending

from odoo import models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def open_stock_barcode_view(self):
        """ method to open the form view of the current record
        from a button on the kanban view
        """
        action = self.env.ref('eg_stock_barcode.stock_picking_details_client_action').read()[0]
        params = {
            'model': 'stock.picking',
            'picking_id': self.id,
            'nomenclature_id': [self.env.company.nomenclature_id.id],
        }
        return dict(action, target='fullscreen', params=params)

    @api.model
    def barcode_stock_picking_data_get(self, picking_id):
        picking_id = self.env['stock.picking'].search([('id', '=', picking_id)])
        group_stock_lot = self.user_has_groups('stock.group_production_lot')
        line_list = []
        for stock_move_line in picking_id.move_line_ids:
            lot_list = []
            stock_lot_ids = self.env['stock.lot'].search(
                [('product_id', '=', stock_move_line.product_id.id)])
            for stock_lot_id in stock_lot_ids:
                lot_list.append(
                    {'lot_id': stock_lot_id.id, 'lot_name': stock_lot_id.name})

            line_dict = {
                'product_id': [stock_move_line.product_id.id, stock_move_line.product_id.display_name],
                'barcode': stock_move_line.product_id.barcode,
                'reserved_uom_qty': stock_move_line.quantity_product_uom,
                'quantity_done': stock_move_line.quantity,
                'lot_id': [stock_move_line.lot_id.id, stock_move_line.lot_id.name],
                'line_id': stock_move_line.id,
                'product_tracking': stock_move_line.product_id.tracking,
                'lot_list': lot_list,
            }
            line_list.append(line_dict)

        return_dict = {
            'message': 'Delivery order found successfully!!!',
            'order': picking_id.name,
            'order_data': {
                'location_id': [picking_id.location_id.id, picking_id.location_id.display_name],
                'location_dest_id': [picking_id.location_dest_id.id,
                                     picking_id.location_dest_id.display_name],
                'partner_id': [picking_id.partner_id.id, picking_id.partner_id.display_name],
                'scheduled_date': picking_id.scheduled_date,
                'state': dict(self._fields['state'].selection).get(picking_id.state),
                'origin': picking_id.origin,
                'use_create_lots': picking_id.picking_type_id.use_create_lots,
                'use_existing_lots': picking_id.picking_type_id.use_existing_lots,
                'group_stock_lot': group_stock_lot,
                'picking_type_code':picking_id.picking_type_code,
            },
            'orderlines': line_list,
        }
        return return_dict

    @api.model
    def open_picking_order(self, picking_id):
        stock_picking_id = self.search([('id', '=', picking_id), ('company_id', '=', self.env.company.id)], limit=1)
        if stock_picking_id:
            return self.picking_order_return_action(picking_id=stock_picking_id)

    @api.model
    def edit_done_qty(self, line_id, done_quantity, lot_number):
        stock_move_line_id = self.env['stock.move.line'].search([('id', '=', line_id)])
        picking_id = self.search(
            [('id', '=', stock_move_line_id.picking_id.id), ('company_id', '=', self.env.company.id)])
        if picking_id.state in ['waiting', 'confirmed', 'assigned']:
            if stock_move_line_id.product_id.tracking == 'lot' and (
                    picking_id.picking_type_id.use_create_lots or picking_id.picking_type_id.use_existing_lots):
                stock_lot_id = self.env['stock.lot'].search([('name', '=', lot_number)])
                if stock_lot_id:
                    lot_id = stock_lot_id.id
                else:
                    stock_lot_id = self.env['stock.lot'].create({
                        'product_id': stock_move_line_id.product_id.id,
                        'company_id': self.env.user.company_id.id,
                        'name': lot_number,
                    })
                    lot_id = stock_lot_id.id
                stock_move_line_id.write({
                    'quantity': done_quantity,
                    'lot_id': lot_id,
                })
            else:
                stock_move_line_id.write({
                    'quantity': done_quantity,
                })
            return self.picking_order_return_action(picking_id=picking_id, updated_line_id=stock_move_line_id.id)
        else:
            return {
                'message': 'Record can be updated only if state is in Ready or Waiting state.'
            }

    @api.model
    def add_new_order_line(self, product_barcode, picking_id):
        """
        Add New stock pack operation line when new product barcode found or already product in stock pack operation so
        add a (1) quantity
        :param product_barcode:
        :param order_barcode:
        :return: return dict
        """
        picking_id = self.search([('id', '=', picking_id), ('company_id', '=', self.env.company.id)])
        if picking_id.state in ['waiting', 'confirmed', 'assigned']:
            product_id = self.env['product.product'].search([('barcode', '=', product_barcode)])
            if product_id:
                stock_move_line_id = self.env['stock.move.line'].search(
                    [('picking_id', '=', picking_id.id), ('product_id', '=', product_id.id)], limit=1)
                if stock_move_line_id:
                    quantity_done = stock_move_line_id.quantity + 1
                    stock_move_line_id.write({
                        'quantity': quantity_done,
                    })

                    return self.picking_order_return_action(picking_id=picking_id,
                                                            updated_line_id=stock_move_line_id.id)
                else:
                    stock_move_line_obj = self.env['stock.move.line']
                    new_stock_move_line_id = stock_move_line_obj.create({
                        'product_id': product_id.id,
                        'quantity': 1,
                        'picking_id': picking_id.id,
                        'product_uom_id': product_id.uom_id.id,
                        'location_id': picking_id.location_id.id,
                        'location_dest_id': picking_id.location_dest_id.id,
                        'state': picking_id.state,
                    })
                    return self.picking_order_return_action(picking_id=picking_id,
                                                            updated_line_id=new_stock_move_line_id.id)

            stock_lot_id = self.env['stock.lot'].search([('name', '=', product_barcode)],
                                                                              limit=1)
            if not product_id and stock_lot_id:
                stock_move_line_id = self.env['stock.move.line'].search(
                    [('picking_id', '=', picking_id.id), ('lot_id', '=', stock_lot_id.id)])
                if stock_move_line_id:
                    quantity_done = stock_move_line_id.quantity + 1
                    stock_move_line_id.write({
                        'quantity': quantity_done,
                    })
                    return self.picking_order_return_action(picking_id=picking_id,
                                                            updated_line_id=stock_move_line_id.id)
                else:
                    stock_move_line_obj = self.env['stock.move.line']
                    new_stock_move_line_id = stock_move_line_obj.create({
                        'product_id': stock_lot_id.product_id.id,
                        'quantity': 1,
                        'picking_id': picking_id.id,
                        'product_uom_id': stock_lot_id.product_id.uom_id.id,
                        'location_id': picking_id.location_id.id,
                        'location_dest_id': picking_id.location_dest_id.id,
                        'lot_id': stock_lot_id.id,
                        'state': picking_id.state,
                    })
                    return self.picking_order_return_action(picking_id=picking_id,
                                                            updated_line_id=new_stock_move_line_id.id)

            if not (product_id and stock_lot_id):
                return {
                    'message': 'Product or Lot Product not found for {} Barcode'.format(product_barcode)
                }
        else:
            return {
                'message': 'Product can be added only in Ready or Waiting state.'
            }

    @api.model
    def mark_as_todo_order(self, picking_id):
        """
        action confirm order when order in a draft state and not add product or edit quantity when other state
        :param order_barcode:
        :return: return_dict
        """
        picking_id = self.search([('id', '=', picking_id)])
        if picking_id.state in ['draft']:
            picking_id.action_confirm()
            return self.picking_order_return_action(picking_id=picking_id, updated_line_id=None)
        else:
            return {
                'message': 'This order is in Draft State first mark as TODO and then after add scan barcode!!!'
            }

    @api.model
    def validate_picking_order(self, picking_id):
        """
        Validate a Order
        :param order_barcode:
        :return: return_dict
        """
        picking_id = self.search([('id', '=', picking_id)])
        if picking_id.state in ['waiting', 'confirmed', 'assigned']:
            action = picking_id.button_validate()
            if action is not True:
                return action
            else:
                return self.picking_order_return_action(picking_id=picking_id)
        else:
            return {
                'message': 'You can not validate order which are already in done or cancel state!!!'
            }

    @api.model
    def clear_lines(self, picking_id):
        """
        Clear Existing lines on delivery
        :return: return_dict
        """
        picking_id = self.search([('id', '=', picking_id)])
        if picking_id.state in ['waiting', 'confirmed', 'assigned']:
            for move in picking_id.move_ids:
                move._do_unreserve()
        result = self.picking_order_return_action(picking_id=picking_id)
        if picking_id.state in ['waiting', 'confirmed', 'assigned']:
            result["message"] = "Lines Cleared Successfully!!!!"
        else:
            result["message"] = "You can not clear lines for transfers which are in draft,done or cancel state!!!"
        return result

    def picking_order_return_action(self, picking_id=None, updated_line_id=None):
        group_stock_lot = self.user_has_groups('stock.group_production_lot')
        line_list = []
        for stock_move_line in picking_id.move_line_ids:
            lot_list = []
            stock_lot_ids = self.env['stock.lot'].search(
                [('product_id', '=', stock_move_line.product_id.id)])
            for stock_lot_id in stock_lot_ids:
                lot_list.append(
                    {'lot_id': stock_lot_id.id, 'lot_name': stock_lot_id.name})

            line_dict = {
                'product_id': [stock_move_line.product_id.id, stock_move_line.product_id.display_name],
                'barcode': stock_move_line.product_id.barcode,
                'reserved_uom_qty': stock_move_line.quantity_product_uom,
                'quantity_done': stock_move_line.quantity,
                'lot_id': [stock_move_line.lot_id.id, stock_move_line.lot_id.name],
                'line_id': stock_move_line.id,
                'product_tracking': stock_move_line.product_id.tracking,
                'lot_list': lot_list,
            }
            line_list.append(line_dict)

        return_dict = {
            'message': 'Delivery order found successfully!!!',
            'order': picking_id.name,
            'order_data': {
                'location_id': [picking_id.location_id.id, picking_id.location_id.display_name],
                'location_dest_id': [picking_id.location_dest_id.id,
                                     picking_id.location_dest_id.display_name],
                'partner_id': [picking_id.partner_id.id, picking_id.partner_id.display_name],
                'scheduled_date': picking_id.scheduled_date,
                'state': dict(self._fields['state'].selection).get(picking_id.state),
                'origin': picking_id.origin,
                'use_create_lots': picking_id.picking_type_id.use_create_lots,
                'use_existing_lots': picking_id.picking_type_id.use_existing_lots,
                'group_stock_lot': group_stock_lot,
                'picking_type_code': picking_id.picking_type_code,
            },
            'orderlines': line_list,
            'updated_line_id': updated_line_id,
        }
        return return_dict

    @api.model
    def open_picking_order(self, picking_id):
        """
        when validate order and show popup after any action perform like backorder after show main page
        """
        stock_picking_id = self.search([('id', '=', picking_id), ('company_id', '=', self.env.company.id)], limit=1)
        if stock_picking_id:
            return self.picking_order_return_action(picking_id=stock_picking_id,
                                                    updated_line_id=False)
