# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from odoo import api, fields, models
from odoo.exceptions import UserError

class ApexSaleOrder(models.Model):
    _name = "apex.sale.order"
    _inherit = ['mail.thread']
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
        self.state = 'accounts_check'
        return True

    def action_accounts_validate(self):
        """ Change state to Validated """
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



