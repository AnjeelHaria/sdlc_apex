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