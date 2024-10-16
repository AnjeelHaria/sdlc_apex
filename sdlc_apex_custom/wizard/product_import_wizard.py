from odoo import models, fields, api
import csv
import base64
import io

class ProductImportWizard(models.TransientModel):
    _name = 'product.import.wizard'
    _description = 'Product Import Wizard'

    file = fields.Binary(string='CSV File', required=True)
    filename = fields.Char(string='File Name')

    def import_products(self):
        if not self.file:
            return

        decoded_file = base64.b64decode(self.file)
        data = io.StringIO(decoded_file.decode('utf-8'))
        reader = csv.DictReader(data)

        product_tmpl_obj = self.env['product.template']
        for row in reader:
            article = row['ARTICLE']
            colour = row['COLOUR']
            sh = row['SOFT/HARD']
            size = row['SIZES']

            # Create list of non-blank variables for name and default code
            name_parts = [part for part in [article, colour, size] if part]
            code_parts = [part for part in [article, colour, sh, size] if part]

            # Construct product name and default code
            product_name = " ".join(name_parts)
            default_code = "-".join(code_parts)

            existing_products = product_tmpl_obj.search([('default_code', '=', default_code)])
            if existing_products:
                # Update existing product
                # product_id = existing_products[0]
                # product_tmpl_obj.write(product_id, {
                #     'name': product_name,
                #     'default_code': default_code
                # })
                print('Existing product found %s %s', existing_products, default_code)
            else:
                # Create new product
                if sh == 'S/H':
                    prod_soft = product_tmpl_obj.create({
                        'name': product_name + ' ' + 'Soft A',
                        'default_code': default_code + '-' + 'Soft A',
                        'article': article,
                        'colour': colour,
                        'hardness_type': 'S',
                        'size': size,
                        # 'categ_id': 1,  # Assuming 'All' category, change as needed
                        # 'list_price': 0.0  # Set appropriate price
                    })
                    product_tmpl_obj.create({
                        'name': product_name + ' ' + 'Soft B',
                        'default_code': default_code + '-' + 'Soft B',
                        'type': 'product',
                        'article': article,
                        'colour': colour,
                        'hardness_type': 'S',
                        'size': size,
                        # 'categ_id': 1,  # Assuming 'All' category, change as needed
                        # 'list_price': 0.0  # Set appropriate price
                    })
                    print(prod_soft.name)
                    prod_hard = product_tmpl_obj.create({
                        'name': product_name + ' ' + 'Hard A',
                        'default_code': default_code + '-' + 'Hard A',
                        'type': 'product',
                        'article': article,
                        'colour': colour,
                        'hardness_type': 'H',
                        'size': size,
                        # 'categ_id': 1,  # Assuming 'All' category, change as needed
                        # 'list_price': 0.0  # Set appropriate price
                    })
                    product_tmpl_obj.create({
                        'name': product_name + ' ' + 'Hard B',
                        'default_code': default_code + '-' + 'Hard B',
                        'type': 'product',
                        'article': article,
                        'colour': colour,
                        'hardness_type': 'H',
                        'size': size,
                        # 'categ_id': 1,  # Assuming 'All' category, change as needed
                        # 'list_price': 0.0  # Set appropriate price
                    })
                    print(prod_hard.name)

                elif sh == 'H':
                    prod_hard = product_tmpl_obj.create({
                        'name': product_name + ' ' + 'Hard A',
                        'default_code': default_code + '-' + 'Hard A',
                        'type': 'product',
                        'article': article,
                        'colour': colour,
                        'hardness_type': 'H',
                        'size': size,
                        # 'categ_id': 1,  # Assuming 'All' category, change as needed
                        # 'list_price': 0.0  # Set appropriate price
                    })
                    product_tmpl_obj.create({
                        'name': product_name + ' ' + 'Hard B',
                        'default_code': default_code + '-' + 'Hard B',
                        'type': 'product',
                        'article': article,
                        'colour': colour,
                        'hardness_type': 'H',
                        'size': size,
                        # 'categ_id': 1,  # Assuming 'All' category, change as needed
                        # 'list_price': 0.0  # Set appropriate price
                    })
                elif sh == 'S':
                    prod_soft = product_tmpl_obj.create({
                        'name': product_name + ' ' + 'Soft A',
                        'default_code': default_code + '-' + 'Soft A',
                        'type': 'product',
                        'article': article,
                        'colour': colour,
                        'hardness_type': 'S',
                        'size': size,
                        # 'categ_id': 1,  # Assuming 'All' category, change as needed
                        # 'list_price': 0.0  # Set appropriate price
                    })
                    product_tmpl_obj.create({
                        'name': product_name + ' ' + 'Soft B',
                        'default_code': default_code + '-' + 'Soft B',
                        'type': 'product',
                        'article': article,
                        'colour': colour,
                        'hardness_type': 'S',
                        'size': size,
                        # 'categ_id': 1,  # Assuming 'All' category, change as needed
                        # 'list_price': 0.0  # Set appropriate price
                    })
                else:
                    prod_soft = product_tmpl_obj.create({
                        'name': product_name + ' ' + 'A',
                        'default_code': default_code + '-' + 'A',
                        'type': 'product',
                        'article': article,
                        'colour': colour,
                        'size': size,
                        # 'categ_id': 1,  # Assuming 'All' category, change as needed
                        # 'list_price': 0.0  # Set appropriate price
                    })
                    product_tmpl_obj.create({
                        'name': product_name + ' ' + 'B',
                        'default_code': default_code + '-' + 'B',
                        'type': 'product',
                        'article': article,
                        'colour': colour,
                        'size': size,
                        # 'categ_id': 1,  # Assuming 'All' category, change as needed
                        # 'list_price': 0.0  # Set appropriate price
                    })



    # def update_attr_dict(self,article,colour,sh,size,attributes_values):
    #     product_tmpl_obj = self.env['product.template']
    #     product_variant_obj = self.env['product.product']
    #     attribute_obj = self.env['product.attribute']
    #     attribute_value_obj = self.env['product.attribute.value']
    #     # Colour attribute
    #     colour_attr = attribute_obj.search([('name', '=', 'Colour')], limit=1)
    #     if not colour_attr:
    #         colour_attr = attribute_obj.create({'name': 'Colour'})
    #     attributes_values['colour']['att_id'] = colour_attr.id
    #
    #     colour_value = attribute_value_obj.search(
    #         [('attribute_id', '=', colour_attr.id), ('name', '=', colour)],
    #         limit=1)
    #     if not colour_value:
    #         colour_value = attribute_value_obj.create({'attribute_id': colour_attr.id, 'name': colour})
    #     if colour_value.id not in attributes_values['colour']['att_value_ids']:
    #         attributes_values['colour']['att_value_ids'].append(colour_value.id)
    #
    #     # Soft/Hard attribute
    #     sh_attr = attribute_obj.search([('name', '=', 'Soft/Hard')], limit=1)
    #     if not sh_attr:
    #         sh_attr = attribute_obj.create({'name': 'Soft/Hard'})
    #     attributes_values['sh']['att_id'] = sh_attr.id
    #     sh_value = attribute_value_obj.search([('attribute_id', '=', sh_attr.id), ('name', '=', sh)], limit=1)
    #     if not sh_value:
    #         sh_value = attribute_value_obj.create({'attribute_id': sh_attr.id, 'name': sh})
    #     if sh_value.id not in attributes_values['sh']['att_value_ids']:
    #         attributes_values['sh']['att_value_ids'].append(sh_value.id)
    #
    #     # Size attribute
    #     size_attr = attribute_obj.search([('name', '=', 'Size')], limit=1)
    #     if not size_attr:
    #         size_attr = attribute_obj.create({'name': 'Size'})
    #     attributes_values['size']['att_id'] = size_attr.id
    #     size_value = attribute_value_obj.search([('attribute_id', '=', size_attr.id), ('name', '=', size)],
    #                                             limit=1)
    #     if not size_value:
    #         size_value = attribute_value_obj.create({'attribute_id': size_attr.id, 'name': size})
    #     if size_value.id not in attributes_values['size']['att_value_ids']:
    #         attributes_values['size']['att_value_ids'].append(size_value.id)
    #     return attributes_values




    # def import_products(self):
    #     if not self.file:
    #         return
    #
    #     decoded_file = base64.b64decode(self.file)
    #     data = io.StringIO(decoded_file.decode('utf-8'))
    #     reader = csv.DictReader(data)
    #
    #     product_tmpl_obj = self.env['product.template']
    #     product_variant_obj = self.env['product.product']
    #     attribute_obj = self.env['product.attribute']
    #     attribute_value_obj = self.env['product.attribute.value']
    #
    #     attributes_values = {
    #         'colour': {'att_id': '', 'att_value_ids': []},
    #         'sh': {'att_id': '', 'att_value_ids': []},
    #         'size': {'att_id': '', 'att_value_ids': []},
    #                          }
    #     stored_article = ''
    #     for row in reader:
    #         article = row['ARTICLE']
    #         colour = row['COLOUR']
    #         sh = row['SOFT/HARD']
    #         size = row['SIZES']
    #
    #         if stored_article == article:
    #             # Getting Ids
    #             attributes_values = self.update_attr_dict(article,colour,sh,size,attributes_values)
    #
    #             continue
    #         else:
    #             # update previous template
    #             stored_template = product_tmpl_obj.search([('name', '=', stored_article)], limit=1)
    #             print(stored_article)
    #             if stored_template:
    #                 stored_template.write({
    #                     "attribute_line_ids": [
    #                         [0, 0, {"attribute_id": attributes_values['colour']['att_id'],
    #                                 "value_ids": [[6, 0, attributes_values['colour']['att_value_ids']]]}],
    #                         [0, 0, {"attribute_id": attributes_values['sh']['att_id'],
    #                                 "value_ids": [[6, 0, attributes_values['sh']['att_value_ids']]]}],
    #                         [0, 0, {"attribute_id": attributes_values['size']['att_id'],
    #                                 "value_ids": [[6, 0, attributes_values['size']['att_value_ids']]]}],
    #                     ],
    #                 })
    #
    #             # Create new template
    #             template = product_tmpl_obj.search([('default_code', '=', article)], limit=1)
    #             if not template:
    #                 template = product_tmpl_obj.create({
    #                     'name': article,
    #                     # 'default_code': article,
    #                     'type': 'product',
    #                 })
    #             stored_article = article
    #             attributes_values['colour']['att_value_ids'] = []
    #             attributes_values['sh']['att_value_ids'] = []
    #             attributes_values['size']['att_value_ids'] = []
    #             attributes_values = self.update_attr_dict(article,colour,sh,size,attributes_values)


