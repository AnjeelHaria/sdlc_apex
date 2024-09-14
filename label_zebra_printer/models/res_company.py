# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

from odoo import fields, models


class Company(models.Model):
    _inherit = 'res.company'

    printer_ids = fields.Many2many('label.printer', string='Printers')
    qz_certificate = fields.Text(string="QZ Certificate")
    private_key = fields.Text()


class LabelPrinters(models.Model):
    _name = 'label.printer'
    _description = 'Label Printers'

    name = fields.Char()
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.user.company_id.id)
