# -*- coding: utf-8 -*-
import datetime
from odoo import models, fields, api, _
import logging

from lxml import etree

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    article = fields.Char()
    colour = fields.Char()
    hardness_type = fields.Char()
    size = fields.Char()


    def create_lot_sequence_auto(self):
        products = self.env['product.template'].search([])
        for product in products:
            if not product.lot_sequence_id:
                product.write({
                    'tracking': 'serial',
                    'auto_create_lot': True,
                    'lot_sequence_prefix': product.default_code+' -'
                })