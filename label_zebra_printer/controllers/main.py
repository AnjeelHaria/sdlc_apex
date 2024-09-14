# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

import json

from odoo.http import Controller, route, request


class ReportController(Controller):
    @route([
        '/zebra/report/<converter>/<reportname>',
        '/zebra/report/<converter>/<reportname>/<docids>',
    ], type='json')
    def report_routes_cusrome(self, reportname, docids=None, **data):
        context = dict(request.env.context)
        if docids:
            docids = [int(i) for i in docids.split(',')]
        if data.get('options'):
            data.update(json.loads(data.pop('options')))
        if data.get('context'):
            data['context'] = json.loads(data['context'])
            if data['context'].get('lang'):
                del data['context']['lang']
            context.update(data['context'])
        data = []
        if reportname == 'label_zebra_printer.report_zebra_shipmentlabel':
            for picking in request.env['stock.picking'].browse(docids):
                data.append({
                    'label': picking.name,
                })
        elif reportname == 'stock.report_location_barcode':
            for location in request.env['stock.location'].browse(docids):
                data.append({
                    'name': location.name,
                    'barcode': location.barcode,
                })
        elif reportname == 'stock.label_product_product_view':
            products = request.env['product.template'].search([('id', 'in', docids)])
            if not products:
                products = request.env['product.product'].search([('id', 'in', docids)])
            for product in products:
                data.append({
                    'name': product.name,
                    'barcode': product.barcode,
                })
        else:
            products = request.env['product.template'].search([('id', 'in', docids)])
            if not products:
                products = request.env['product.product'].search([('id', 'in', docids)])
            for product in products:
                data.append({
                    'name': product.name,
                    'barcode': product.barcode,
                })
        
        return {'data': data}
