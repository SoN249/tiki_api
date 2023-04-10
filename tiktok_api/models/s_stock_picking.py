from odoo import fields, models
import json
import urllib3

urllib3.disable_warnings()


class SStockPickings(models.Model):
    _inherit = "stock.picking"
    package_tiktok_id = fields.Char('Package Tiktok')
    delivery_option = fields.Selection([('1',"STANDARD"),
                                        ('2',"EXPRESS"),
                                        ('3',"ECONOMY"),
                                        ('4',"SEND_BY_SELLER")
                                        ], string="Tùy chọn vận chuyển")
    package_status = fields.Selection([('1','TO_FULFILL'),
                                       ('2','PROCESSING'),
                                       ('3','FULFILLING'),
                                       ('4','COMPLETED'),
                                       ('5','CANCELLED')
                                       ], string="Trạng thái giao hàng")

    def get_packages(self):
        api = "/api/fulfillment/search"
        payload = {
            "page_size": 50
        }

        response = self.env["integrate.tiktok"]._post_data_tiktok(api, json.dumps(payload))
        data = json.loads(response)

        return data['data']

    def get_package_detail(self,package_id):
        api = "/api/fulfillment/detail"
        param={"package_id":package_id}
        response = self.env["integrate.tiktok"]._get_data_tiktok(api,param=param)
        data = json.loads(response)
        return data['data']

    def sync_package(self):
        package_id = self.get_packages()
        for id in package_id['package_list']:
            package = self.get_package_detail(id['package_id'])
            sale_order = self.env['sale.order'].search([('tiktok_order_id','=',package['order_info_list'][0]['order_id'])])
            if sale_order:
                package_id = self.sudo().search([('sale_id','=', sale_order.id),("state",'!=','cancel')])

                value = {
                    "package_status": str(package['package_status']),
                    "package_tiktok_id": package['package_id'],
                    "delivery_option": str(package['delivery_option'])
                }
                if package['package_id'] not in self.search([]).mapped('package_tiktok_id'):
                    package_id.sudo().write(value)


