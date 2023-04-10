from odoo import fields, models
import json
import urllib3

urllib3.disable_warnings()
class SOrderTiktok(models.Model):
    _inherit = "sale.order"

    tiktok_order_id = fields.Char("Tiktok ID")
    is_tiktok_order = fields.Boolean("Đơn hàng Tiktok", default=False)
    order_status = fields.Selection([("100","UNPAID"),
                                     ("111","AWAITING_SHIPMENT"),
                                     ("112","AWAITING_COLLECTION"),
                                     ("114","PARTIALLY_SHIPPING"),
                                     ("121","IN_TRANSIT"),
                                     ("122","DELIVERED"),
                                     ("130","COMPLETED"),
                                     ("140","CANCELLED")], string="Trạng thái đơn hàng")

    def get_order(self):
        api = "/api/orders/search"
        payload ={
            "page_size": 20
        }
        cursor = self.env['order.cursor'].sudo().search([])
        if cursor:
            payload.update({"cursor": cursor[-1].next_cursor})
        response = self.env["integrate.tiktok"]._post_data_tiktok(api, json.dumps(payload))
        data = json.loads(response)
        if 'order_list' in data['data']:
            self.env['order.cursor'].sudo().create({"next_cursor":data['data']['next_cursor'],"more":data['data']['more']})
            return data['data']
        else:
            return False
    def get_order_details(self,order_id):
        api = "/api/orders/detail/query"

        payload = json.dumps({
            "order_id_list":[order_id]
        })
        response = self.env["integrate.tiktok"]._post_data_tiktok(api, payload)
        data = json.loads(response)
        return data['data']


    def sync_data_order(self):
            order_id = self.get_order()
            while order_id != False:
                print(order_id)

            # for id in order_id['order_list']:
                # order = self.get_order_details(id['order_id'])
                # warehouse_id = self.env["stock.warehouse"].sudo().search([("warehouse_tiktok_id",'=',order['order_list'][0]['warehouse_id'])])
                # values = {
                #     "partner_id": "24",
                #     "pricelist_id": '1',
                #     "partner_invoice_id":24,
                #     "partner_shipping_id":24,
                #     "tiktok_order_id": order['order_list'][0]['order_id'],
                #     "is_tiktok_order": True,
                #     "order_status": str(order['order_list'][0]['order_status']),
                #     "warehouse_id": warehouse_id.id,
                #     "currency_id": 2
                # }
                # if id['order_id']  not in self.search([]).mapped("tiktok_order_id"):
                #     order_id = self.create(values)
                #     order_id.sudo().search([]).write({"currency_id": 2})
                #     order_id.order_line.sudo().create([{
                #         "order_id": order_id.id,
                #         "product_id": 21,
                #         "product_uom_qty": 3},
                #         {
                #             "order_id": order_id.id,
                #             "product_id": 24,
                #             "product_uom_qty": 3}
                #
                #     ])
                #     order_id.action_confirm()


class OrderCursor(models.Model):
    _name='order.cursor'
    next_cursor = fields.Char("Cursor")
    more = fields.Boolean('More')


