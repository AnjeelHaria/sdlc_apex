from odoo import models, fields

class Apex_Sale_Order_Validate_Wizard(models.TransientModel):
    _name = 'apex.sale.order.validate.wizard'
    _description = 'Apex Sale Order Validate Wizard'

    comments = fields.Text()
    apex_sale_order_id = fields.Many2one("apex.sale.order")

    def validate_order(self):
        self.apex_sale_order_id.state = 'validated'
        if self.comments:
            msg = ("Order validated by %s with comment:%s" % (self.env.user.name, self.comments))
        else:
            msg = ("Order validated by %s" % self.env.user.name)
        self.apex_sale_order_id.message_post(
            body=msg,
            subtype_xmlid='mail.mt_note',
        )
        self.apex_sale_order_id.sale_order_id.is_validated_by_accounts = True
        self.apex_sale_order_id.sale_order_id.message_post(
            body=msg,
            subtype_xmlid='mail.mt_note',
        )
        return True
