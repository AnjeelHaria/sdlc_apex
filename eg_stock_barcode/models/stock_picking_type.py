from odoo import models


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    def get_stock_picking_action_picking_type_kanban(self):
        """
        This Method used for when Operation type in kanaban view when click when filter a redy state or selected
         default odoo v13 contex pass of deafult_picking_id and search_picking_id in _get_action method but odoo v13 to
         down version Manully Context pass of stock_picking_id and defualt_picking_id
        :return: action
        """
        return self._get_action('eg_stock_barcode.stock_picking_action_kanban_for_stock_barcode')
