from odoo import fields, models
import json
import http.client

class WarehousesSeller(models.Model):
    _name = "warehouses.seller"

    warehouses_id = fields.Id("Id")
    name = fields.Text("Name")
    status = fields.Char("Status")
    street = fields.Text("Street")
    country_name = fields.Char("Country Name")
    country_code = fields.Char("Country Code")
    region_name = fields.Char("Region Name")
    region_code = fields.Char("Region Code")
    district_name = fields.Char("District Name")
    district_code = fields.Char("District Code")
    ward_name = fields.Char("Ward Name")
    ward_code = fields.Char("Ward Code")

    def get_warehouses_seller(self):
        conn = http.client.HTTPSConnection("api.tiki.vn")
        payload = ''
        data_conn = self.env['base.integrate.tiki'].sudo().search([])
        headers = {
            'tiki-api': data_conn.tiki_api
        }
        conn.request("GET",
                     "/integration/v2/sellers/me/warehouses?access_token="+data_conn.access_token,
                     payload, headers)
        res = conn.getresponse()
        response = res.read().decode("utf-8")
        res_json = json.loads(response)
        for res in res_json['data']:
            self.env["warehouses.seller"].sudo().create({
                'warehouses_id': res['id'],
                'name': res['name'],
                'status': res['status'],
                'street': res['street'],
                'country_name': res['country']['name'],
                'country_code': res['country']['code'],
                'district_name': res['district']['name'],
                'district_code': res['district']['code'],
                'ward_name': res['ward']['name'],
                'ward_code': res['ward']['code']
            })