# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ApexSaleOrder(models.Model):
    _name = "apex.sale.order"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Apex Sale Order"

    name = fields.Char(
        string="Order Reference",
        required=True, copy=False, readonly=False,
        index='trigram',
        default=lambda self: 'New')
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    state = fields.Selection([('draft', 'Draft'),
                                ('accounts_check', 'Sent for Accounts Check'),
                              ('validated', 'Validated'),
                              ],default="draft")
    order_line = fields.One2many(
        comodel_name='apex.sale.order.line',
        inverse_name='order_id',
        string="Order Lines",
        copy=True, auto_join=True)
    sale_order_id = fields.Many2one('sale.order')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', "New") == "New":
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'apex.sale.order')
        return super().create(vals_list)

    def action_accounts_check(self):
        """ Change state to Accounts Check """
        self.ensure_one()
        if not self.order_line:
            raise UserError("Add at least one order line")
        order_lines_data = []
        for line in self.order_line:
            order_lines_data.append((0, 0, {
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'product_warehouse_id': line.product_warehouse_id.id,
            }))
        sale_order = self.env['sale.order'].sudo().create({
            'partner_id': self.partner_id.id,
            'order_line': order_lines_data,
            'user_id': self.create_uid.id
        })
        sale_order.action_confirm()
        for picking in sale_order.picking_ids.filtered(lambda p:p.state in ('waiting','draft','confirmed')):
            picking.action_assign()
        self.write({'state':'accounts_check','sale_order_id':sale_order.id})
        for order in self:
            order_ref = order._get_html_link()
            customer_ref = order.partner_id._get_html_link()
            for user in self.env.ref("sdlc_apex_custom.apex_accounts").users:
                order.activity_schedule(
                    'apex_sale_order.act_apex_sale_accounts_check',
                    user_id=user.id,
                    note=_("Check %(order)s for customer %(customer)s", order=order_ref, customer=customer_ref))
        return True

    def action_accounts_validate(self):
        """ Change state to Validated """
        self.activity_unlink(['apex_sale_order.act_apex_sale_accounts_check'])
        self.ensure_one()
        return {
            'name': "Validate Apex Sale Order",
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'apex.sale.order.validate.wizard',
            'target': 'new',
            'context': {
                'default_apex_sale_order_id': self.id
            }
        }

class ApexSaleOrderLine(models.Model):
    _name = "apex.sale.order.line"
    _description = "Apex Sale Order Line"

    order_id = fields.Many2one(
        comodel_name='apex.sale.order',
        string="Order Reference",
        required=True, ondelete='cascade', index=True, copy=False)
    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Product",
        required=True,
        change_default=True, ondelete='restrict', index='btree_not_null',
        domain="[('sale_ok', '=', True)]")
    product_uom_qty = fields.Float(
        string="Quantity",
        digits='Product Unit of Measure', default=1.0,
        required=True)
    product_warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Warehouse', help='Warehouse where product taken from')

    missed_uom_qty = fields.Float(
        string="Missed Quantity",
        digits='Product Unit of Measure', default=1.0,
        required=True)


