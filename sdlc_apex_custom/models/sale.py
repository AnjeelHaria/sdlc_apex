# -*- coding: utf-8 -*-
import datetime
from odoo import models, fields, api, _
import logging

from lxml import etree

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # @api.model
    # def fields_get(self, allfields=None, attributes=None):
    #     fields = super().fields_get(allfields=allfields, attributes=attributes)
    #     fields = {field_name: description for field_name, description in fields.items()}
    #     if self.env.user.has_group('sdlc_apex_custom.apex_sales_operator'):
    #         accessable_fields = ["partner_id","order_line"]
    #         for field_name, description in fields.items():
    #             if field_name not in accessable_fields:
    #                 description['invisible'] = 1
    #                 description['column_invisible'] = 1
    #         return fields
    #     return fields
    #     if self.env.user.has_group('sdlc_apex_custom.apex_sales_operator'):
    #         accessable_fields = ["partner_id","order_line"]
    #         for field_name, description in fields.items():
    #             if field_name not in accessable_fields and not description.get('invisible', False):
    #                 description['invisible'] = True
    #         return fields
    #     readable_fields = self.SELF_READABLE_FIELDS
    #
    #
    #     writable_fields = self.SELF_WRITABLE_FIELDS
    #     for field_name, description in public_fields.items():
    #         if field_name not in writable_fields and not description.get('readonly', False):
    #             # If the field is not in Writable fields and it is not readonly then we force the readonly to True
    #             description['readonly'] = True
    #
    #     return public_fields

    @api.model
    def get_view(self, view_id=None, view_type='form', **options):
        res = super().get_view(view_id, view_type, **options)
        if view_type == 'form' and self.env.user.has_group('sdlc_apex_custom.apex_accounts'):
            accessable_fields = ["partner_id", "order_line"]
            doc = etree.fromstring(res["arch"])
            for node in doc.xpath("//field"):
                if node.attrib and node.attrib.get('name') not in accessable_fields:
                    node.attrib['invisible'] = '1'
                    node.set("invisible", "1")
            res["arch"] = etree.tostring(doc)
        return super().get_view(view_id, view_type, **options)

