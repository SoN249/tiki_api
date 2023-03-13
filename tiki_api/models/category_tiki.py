from odoo import fields, models
import http.client
import json


class CategoryTiki(models.Model):
    _name = 'categories.tiki'

    categories_id = fields.Integer('ID')
    name = fields.Char(string='Tên category')
    parent_id = fields.Integer('Parent')
    is_primary = fields.Boolean('Is primary')
    is_product_listing_enabled = fields.Boolean('Is product listing enabled')
    no_license_seller_enabled = fields.Boolean('No license seller enabled')

    def get_categories_tiktok(self):
        conn = http.client.HTTPSConnection("api.tiki.vn")
        data_conn = self.env['base.integrate.tiki'].sudo().search([])
        payload = ''
        headers = {
            'Authorization': 'Bearer ' + data_conn.access_token
        }
        conn.request("GET", "/integration/v2/categories?name&parent", payload, headers)
        res = conn.getresponse()
        response = res.read().decode("utf-8")
        res_json = json.loads(response)
        for res in res_json['data']:
            self.env['categories.tiki'].sudo().create({
                'categories_id': res['id'],
                'name': res['name'],
                'is_primary': res['is_primary'],
                'parent_id': res['parent_id'],
                'is_product_listing_enabled': res['is_product_listing_enabled'],
                'no_license_seller_enabled': res['no_license_seller_enabled']
            })
