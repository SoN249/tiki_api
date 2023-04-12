from odoo import fields, models
import json
from odoo.exceptions import ValidationError
class ShippingDocumentType(models.Model):
    _name="shipping.document"

    document_type = fields.Selection([('SHIPPING_LABEL', "Shipping Label"),
                                      ('PICK_LIST', 'Pick List'),
                                      ('SL_PL', 'Both')
                                      ], required = True, default="SL_PL")
    document_size = fields.Selection([('A5', "A5"),
                                      ('A6', "A6"),
                                      ], default = 'A6')

    def btn_confirm(self):
        order_id = self.env.context.get('order_id')

        api = "/api/logistics/shipping_document"
        param = {
                "order_id": order_id,
                 "document_type": self.document_type,
                 "document_size": self.document_size
                 }
        response = self.env["integrate.tiktok"]._get_data_tiktok(api, param=param)
        data = json.loads(response)
        if data['data']:
            url = data['data']['doc_url']
            return {
                'name': 'Shipping Document',
                'type': 'ir.actions.act_url',
                'url': url,
                'target': 'new',
            }
        else:
            raise  ValidationError("Không có dữ liệu shipping document ")
