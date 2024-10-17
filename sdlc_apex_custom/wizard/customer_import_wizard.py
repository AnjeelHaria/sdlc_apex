from odoo import models, fields, api
import csv
import base64
import io
import logging
_logger = logging.getLogger(__name__)

class CustomerImportWizard(models.TransientModel):
    _name = 'customer.import.wizard'
    _description = 'Customer Import Wizard'

    file = fields.Binary(string='CSV File', required=True)
    filename = fields.Char(string='File Name')

    def import_customers(self):
        if not self.file:
            return

        decoded_file = base64.b64decode(self.file)
        data = io.StringIO(decoded_file.decode('utf-8'))
        reader = csv.DictReader(data)

        res_partner_obj = self.env['res.partner']
        state_id = self.env['res.country.state']
        country_id = self.env['res.country'].search([
                    ('code', '=', 'IN'),
                ])
        city = ''
        for row in reader:
            print(row['CUSTOMER'])
            if row['CUSTOMER'] == 'SDLC-MUMBAI':
                next_state_id = self.env['res.country.state'].search([
                    ('code', '=', "MH"),
                    ('country_id', '=', country_id.id)
                ], limit=1)
                if next_state_id:
                    state_id = next_state_id
                else:
                    state_id = ''
                city = 'Mumbai'
                continue
            if row['CUSTOMER'] == 'SDLC-SRINAGAR':
                next_state_id = self.env['res.country.state'].search([
                    ('code', '=', "JK"),
                    ('country_id', '=', country_id.id)
                ], limit=1)
                if next_state_id:
                    state_id = next_state_id
                else:
                    state_id = ''
                city = 'Srinagar'
                continue
            if row['CUSTOMER'] == 'SDLC-JAMMU':
                next_state_id = self.env['res.country.state'].search([
                    ('code', '=', "JK"),
                    ('country_id', '=', country_id.id)
                ], limit=1)
                if next_state_id:
                    state_id = next_state_id
                else:
                    state_id = ''
                city = 'Jammu'
                continue
            if 'SDLC-' in row['CUSTOMER']:
                state = row['CUSTOMER'].split('-')[1]
                next_state_id = self.env['res.country.state'].search([
                    ('name', 'ilike', state),
                    ('country_id', '=', country_id.id)
                ],limit=1)
                if next_state_id:
                    state_id = next_state_id
                else:
                    state_id = ''
                city = ''
                continue
            else:

                partner_id = self.env['res.partner'].create({
                    'name': row['CUSTOMER'],
                    'is_company': True,
                    'country_id': country_id.id,
                    'state_id': state_id.id if state_id else '',
                    'city': city if city else ''

                })




