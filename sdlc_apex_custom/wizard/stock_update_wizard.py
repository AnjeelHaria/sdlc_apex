from odoo import models, fields, api
import csv
import base64
import io

class StockUpdateWizard(models.TransientModel):
    _name = 'stock.update.wizard'
    _description = 'Stock Update Wizard'

    file = fields.Binary(string='CSV File', required=True)
    filename = fields.Char(string='File Name')

    def update_stock(self):
        if not self.file:
            return