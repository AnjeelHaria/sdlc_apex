from odoo import models, fields

class Apex_Sale_Order_Validate_Wizard(models.TransientModel):
    _name = 'apex.sale.order.validate.wizard'
    _description = 'Apex Sale Order Validate Wizard'

    comments = fields.Text()
    apex_sale_order_id = fields.Many2one("apex.sale.order")

    def validate_order(self):
        self.apex_sale_order_id.state = 'validated'
        order_lines_data = []
        for line in self.apex_sale_order_id.order_line:
            order_lines_data.append((0, 0, {
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
            }))

        sale_order = self.env['sale.order'].sudo().create({
            'partner_id': self.apex_sale_order_id.partner_id.id,
            'order_line': order_lines_data,
            'user_id': self.apex_sale_order_id.create_uid.id
        })
        if self.comments:
            msg = ("Order validated by %s with comment:%s" % (self.env.user.name, self.comments))
        else:
            msg = ("Order validated by %s" % self.env.user.name)
        self.apex_sale_order_id.message_post(
            body=msg,
            subtype_xmlid='mail.mt_note',
        )
        sale_order.message_post(
            body=msg,
            subtype_xmlid='mail.mt_note',
        )
        return True
