# -*- coding: utf-8 -*-
import datetime
from odoo import models, fields, api, _
import base64
import io
import csv
import logging
import time
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT
from markupsafe import Markup
import os

_logger = logging.getLogger(__name__)

class ResCompanyInherit(models.Model):
    _inherit = 'res.company'

    product_csv = fields.Binary(string='Products File')
    product_csv_filename = fields.Char('Product CSV filename')

    def import_products_apex(self):
        if self.product_csv:
            print('Products Import')
            csv_data = base64.b64decode(self.product_csv)
            data_file = io.StringIO(csv_data.decode("utf-8"))
            data_file.seek(0)
            file_reader = []
            csv_reader = csv.reader(data_file, delimiter=',')
            file_reader.extend(csv_reader)
            count = 0
            for row in file_reader:
                # print(row)
                if count == 0:
                    count = count + 1
                    continue

