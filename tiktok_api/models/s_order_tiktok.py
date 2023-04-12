from odoo import fields, models
import json
import urllib3

urllib3.disable_warnings()
class SOrderTiktok(models.Model):
    _inherit = "sale.order"

    tiktok_order_id = fields.Char("Tiktok ID")
    is_tiktok_order = fields.Boolean("Đơn hàng Tiktok")
    order_status = fields.Selection([("100","UNPAID"),
                                     ("111","AWAITING_SHIPMENT"),
                                     ("112","AWAITING_COLLECTION"),
                                     ("114","PARTIALLY_SHIPPING"),
                                     ("121","IN_TRANSIT"),
                                     ("122","DELIVERED"),
                                     ("130","COMPLETED"),
                                     ("140","CANCELLED")], string="Trạng thái đơn hàng")

    def get_order(self, cursor = None):
        api = "/api/orders/search"
        payload ={
            "page_size": 20
        }
        cursors = self.env['cursor.tiktok'].sudo().search([])
        if not cursor is None:
            payload.update({"cursor": cursor})
        elif cursors:
            payload.update({"cursor": cursors[-1]['next_cursor']})
        response = self.env["integrate.tiktok"]._post_data_tiktok(api, json.dumps(payload))
        data = json.loads(response)
        return data['data']

    def get_order_details(self,order_id):
        api = "/api/orders/detail/query"

        payload = json.dumps({
            "order_id_list":[order_id]
        })
        response = self.env["integrate.tiktok"]._post_data_tiktok(api, payload)
        data = json.loads(response)
        return data['data']

    def sync_data_order(self):
        more = []
        order_list = []
        if not more:
            more.append(True)
        while True in more:
            order_id = self.get_order()
            for id in order_id['order_list']:
                order_list.append(id['order_id'])
                order_detail = self.get_order_details(id['order_id'])
                warehouse_id = self.env["stock.warehouse"].sudo().search([("warehouse_tiktok_id",'=',order_detail['order_list'][0]['warehouse_id'])])
                customer_tiktok = self.env["res.partner"].sudo().search([('is_tiktok_customer','=',True)])
                values = {
                    "partner_id": customer_tiktok.id,
                    "pricelist_id": '1',
                    "partner_invoice_id":customer_tiktok.id,
                    "partner_shipping_id":customer_tiktok.id,
                    "tiktok_order_id": order_detail['order_list'][0]['order_id'],
                    "is_tiktok_order": True,
                    "order_status": str(order_detail['order_list'][0]['order_status']),
                    "warehouse_id": warehouse_id.id,
                }
                if id['order_id']  not in self.search([]).mapped("tiktok_order_id"):
                    order = self.create(values)
                    order.sudo().search([]).write({"currency_id": 2})
                    order.order_line.sudo().create([{
                        "order_id": order.id,
                        "product_id": 21,
                        "product_uom_qty": 3},
                        {
                            "order_id": order.id,
                            "product_id": 24,
                            "product_uom_qty": 3}

                    ])

            if len(order_list) == 20 and order_id['more'] == True:
                more[-1] = order_id['more']
                self.env['cursor.tiktok'].sudo().create(
                    {"next_cursor": order_id['next_cursor'], "more": order_id['more'], 'cursor_type': "order"})
                order_list.clear()
            else:
                break
    def update_order(self):
        next_cursor = self.env['cursor.tiktok'].search([]).mapped('next_cursor')
        next_cursor.insert(0,"")
        for cursor in next_cursor:
           order_id = self.get_order(cursor=cursor)
           for id in order_id['order_list']:
               order_detail = self.get_order_details(id['order_id'])
               order = self.env['sale.order'].sudo().search([('tiktok_order_id','=',order_detail['order_list'][0]['order_id'])])
               if order:
                   order.sudo().write({'order_status':str(order_detail['order_list'][0]['order_status'])})

class OrderCursor(models.Model):
    _name='cursor.tiktok'
    next_cursor = fields.Char("Cursor")
    more = fields.Boolean('More')
    cursor_type = fields.Char("Type")


