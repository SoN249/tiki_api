from odoo import fields, models, api
import http.client
import json
from odoo.exceptions import ValidationError, UserError


class ProductsTiki(models.Model):
    _inherit = ['product.template']

    brand = fields.Many2one('brand.tiki', string="Thương hiệu")
    categories_ids = fields.Many2one('categories.tiki', string="Danh mục sản phẩm",
                                    domain="[('no_license_seller_enabled','=', True)]")
    origin = fields.Many2one('product.origin', string="Xuất xứ (Quốc gia)")
    brand_country = fields.Many2one('product.origin', string="Xuất xứ thương hiệu (Quốc gia)")
    description = fields.Html('Mô tả sản phẩm')
    product_weight_kg = fields.Float('Trọng lượng sau đóng gói (kg)')
    product_length = fields.Float('Chiều dài (cm)')
    product_width = fields.Float('Chiều rộng (cm)')
    product_height = fields.Float('Chiều cao')
    is_warranty_applied = fields.Selection([('0', 'Không có bảo hành'),
                                            ('1', 'Có bảo hành')
                                            ], default="0", string="Sản phẩm có bảo hành không?")
    inventory_type = fields.Selection([('dropship', 'FBT - Hàng lưu kho tiki'),
                                       ('instock', 'Nhà bán tự đóng gói, Tiki giao hàng'),
                                       ], string='Mô hình vận hành')
    warehouse_ids = fields.One2many('warehouses.tiki.line', 'product_id_warehouses', string='Kho Tiki')

    is_auto_turn_on = fields.Boolean('Auto turn', default=False)
    ulr_image = fields.Text('Đường dẫn ảnh tài liệu')
    type_certificate = fields.Selection([('brand', 'Brand')], string="Type")
    track_id = fields.Char(string='Track ID')
    state = fields.Selection([('none', 'New'),
                              ('processing', "Processing"),
                              ('drafted', 'Drafted'),
                              ('bot_awaiting_approve', "Bot Awaiting Approve"),
                              ('md_awaiting_approve', 'MD Awaiting Approve'),
                              ('awaiting_approve', 'Awaiting Approve'),
                              ('approved', 'Approved'),
                              ('rejected', 'Rejected'),
                              ('deleted', 'Deleted')
                              ], default='none')

    @api.onchange('attribute_line_ids')
    def _check_attribute_id(self):
        if len(self.attribute_line_ids.attribute_id) > 2:
            raise ValidationError("Not more than 2 attribute")

    @api.onchange('product_weight_kg', 'product_length', 'product_width', 'product_height', 'product_height')
    def _onchange_info(self):
        if self.product_length < 0 or self.product_weight_kg < 0 or self.product_width < 0 or self.product_height < 0:
            raise ValidationError("Giá trị phải lớn hơn 0")

    def btn_create_product(self):
        conn = http.client.HTTPSConnection("api.tiki.vn")
        data_conn = self.env['base.integrate.tiki'].sudo().search([])
        headers = {
            'tiki-api': data_conn.tiki_api,
            'Authorization': 'Bearer ' + data_conn.access_token,
            'Content-Type': 'application/json'
        }

        data = {
            "category_id": self.categories_ids.categories_id,
            "name": self.name,
            "description": self.description,
            "attributes": {
                "bulky": 0,
                "origin": self.origin.name,
                "brand_country": self.brand_country.name,
                "brand": self.brand.name,
                "product_height": self.product_height,
                "product_width": self.product_width,
                "product_length": self.product_length,
                "product_weight_kg": self.product_weight_kg,
                "is_warranty_applied": self.is_warranty_applied
            },
            "image": 'https://images-na.ssl-images-amazon.com/images/I/715uwlmCWsL.jpg',
            "option_attributes": [],
            "variants": [

            ],
            "certificate_files": [
                {
                    "url": self.ulr_image,
                    "type": self.type_certificate
                }
            ],
            "meta_data": {
                "is_auto_turn_on": self.is_auto_turn_on
            }
        }
        # add warehouses stock
        warehouse_stocks = []
        warehouse_id = self.warehouse_ids.warehouse_id.mapped('warehouses_id')
        qtyAvailable = self.warehouse_ids.mapped('qtyAvailable')
        for warehouse_id, qtyAvailable in zip(warehouse_id, qtyAvailable):
            warehouse_stocks.append({
                "warehouseId": warehouse_id,
                "qtyAvailable": qtyAvailable
            })

        if self.attribute_line_ids:
            data["option_attributes"].extend(self.attribute_line_ids.attribute_id.mapped('name'))

        if len(data["option_attributes"]) == 0:
            data["option_attributes"] = []
            data['variants'].append({
                "sku": self.default_code,
                "price": self.list_price,
                "option1": "none",
                "inventory_type": self.inventory_type,
                "warehouse_stocks": warehouse_stocks,
                "image": "https://images-na.ssl-images-amazon.com/images/I/715uwlmCWsLBY.jpg"
            })
        else:
                if self.product_variant_count > 1:
                    for r in range(len(self.product_variant_ids)):
                        for value in self.product_variant_ids[r]:
                            data['variants'].append({
                                "sku": value.default_code,
                                "price": value.lst_price,
                                "inventory_type": self.inventory_type,
                                "warehouse_stocks": warehouse_stocks,
                                "image": "https://images-na.ssl-images-amazon.com/images/I/715uwlmCWsLBY.jpg",
                            })
                            if len(data['option_attributes']) == 1:
                                data['variants'][r].update({
                                    "option1": value.product_template_variant_value_ids.name,
                                })

                            elif self.attribute_line_ids[0].value_count == 1:
                                data['variants'][r].update({
                                    "option1": self.attribute_line_ids[0].value_ids.name,
                                    "option2": value.product_template_variant_value_ids.name
                                })
                            elif self.attribute_line_ids[1].value_count == 1:
                                data['variants'][r].update({
                                    "option1": value.product_template_variant_value_ids.name,
                                    "option2": self.attribute_line_ids[1].value_ids.name
                                })
                            else:
                                data['variants'][r].update({
                                    "option1": value.product_template_variant_value_ids[0].name,
                                    "option2": value.product_template_variant_value_ids[1].name
                                })

                else:
                    data['variants'].append({
                        "sku": self.default_code,
                        "price": self.list_price,
                        "inventory_type": self.inventory_type,
                        "warehouse_stocks": warehouse_stocks,
                        "image": "https://images-na.ssl-images-amazon.com/images/I/715uwlmCWsLBY.jpg"
                    })
                    if len(data['option_attributes']) == 1:
                        data['variants'][0].update({
                            "option1": self.attribute_line_ids[0].value_ids.name
                        })
                    else:
                        data['variants'][0].update({
                            "option1": self.attribute_line_ids[0].value_ids.name,
                            "option2": self.attribute_line_ids[1].value_ids.name,
                        })


        payload = json.dumps(data)

        conn.request("POST", "/integration/v2.1/requests", payload, headers)
        res = conn.getresponse()
        if res.status == 200:
            response = res.read().decode("utf-8").replace("'", '"')
            res_json = json.loads(response)
            self.track_id = res_json["track_id"]

    def _cron_update_state(self):
        if not self.state:
            self.state = 'none'
        if self.track_id:
          data =  self.env['tracking.tiki']._get_tracking_tiki(self.track_id)
          self.state = data['state']
          self.message_post(body=f'The new plan has been sent.')

