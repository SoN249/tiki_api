from odoo import fields, models
import http.client
import json
class WerehousesTiki(models.Model):
    _name = 'warehouses.tiki'

    warehouses_id = fields.Integer('Id')
    name = fields.Char(string='Tên Kho')
    code = fields.Char(string='Code')


    def get_warehouses_tiki(self):
        conn = http.client.HTTPSConnection("api.tiki.vn")
        data_conn = self.env['base.integrate.tiki'].sudo().search([])
        payload = ''
        headers = {
            'tiki-api': data_conn.tiki_api
        }
        conn.request("GET", "/integration/v2/warehouses/tiki", payload, headers)
        res = conn.getresponse()
        response = res.read().decode("utf-8")
        res_json = json.loads(response)
        for data in res_json:
            self.env['warehouses.tiki'].sudo().create({
                "warehouses_id": data['id'],
                "name": data['name'],
                "code": data['code']
            })
class  WerehousesTikiLine(models.Model):
    _name ="warehouses.tiki.line"

    attribute_id = fields.Many2one('warehouses.tiki', string='Kho')
    qtyAvailable = fields.Integer('Số lượng trong kho')
    product_id_warehouses = fields.Many2one('product.product',string='Product')