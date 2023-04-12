from odoo import fields, models
import json

class SStockTiktok(models.Model):
    _inherit = "stock.warehouse"
    is_warehouse_tiktok = fields.Boolean("Is stock tiktok")
    warehouse_tiktok_id = fields.Char("Warehouse Tiktok")

    def get_warehouse_list(self):
        api = "/api/logistics/get_warehouse_list"
        param = {"shop_id": ""}
        response = self.env["integrate.tiktok"]._get_data_tiktok(api, param=param)
        data = json.loads(response)

        return data['data']

    def sync_warehouse(self):
        warehouse_id = self.get_warehouse_list()
        for warehouse in warehouse_id['warehouse_list']:
            partner_value = {
                "name": warehouse['warehouse_address']['full_address'],
                "is_company": "True",
                "street":warehouse['warehouse_address']['full_address'],
                "city": warehouse['warehouse_address']['city'],
                "zip": warehouse['warehouse_address']['zipcode'],

            }
            res = self.env['res.partner'].sudo().create(partner_value)
            values = {
                "name": warehouse['warehouse_name'],
                "warehouse_tiktok_id": warehouse['warehouse_id'],
                "partner_id": res.id,
                "is_warehouse_tiktok":"True",
                "view_location_id": 7,
                "code":warehouse['warehouse_name']
            }
            if warehouse['warehouse_id'] not in self.sudo().search([]).mapped("warehouse_tiktok_id"):
                self.sudo().create(values)

