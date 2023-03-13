from odoo import fields, models, api
import http.client
import json
from odoo.exceptions import ValidationError, UserError


class ProductsTiki(models.Model):
    _inherit = ['product.product']

    attribute_id = fields.One2many('product.attribute', 'product_id', limit=2)
    brand = fields.Many2one('brand.tiki', string="Thương hiệu")
    categ_id = fields.Many2one('categories.tiki', string="Danh mục sản phẩm")
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

    image = fields.Image(string="Ảnh sản phẩm")
    is_auto_turn_on = fields.Boolean('Auto turn', default=False)
    ulr_image = fields.Text('Đường dẫn ảnh tài liệu')
    type_certificate = fields.Selection([('brand', 'Brand')], string="Type")
    price = fields.Float('Giá bán')
    sku = fields.Char(string='Mã sản phẩm')
    is_option = fields.Boolean('Có thêm lựa chọn sản phẩm?', default=False)
    track_id = fields.Char(string='Track ID')

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
            "category_id": self.categ_id.categories_id,
            "name": self.name,
            "description": self.description,
            "attributes": {
                "bulky": 0,
                "origin": self.origin.name,
                "brand_country": self.brand_country.name,
                "brand": self.brand,
                "product_height": self.product_height,
                "product_width": self.product_width,
                "product_length": self.product_length,
                "product_weight_kg": self.product_weight_kg,
                "is_warranty_applied": self.is_warranty_applied
            },
            "image": "https://i1.sndcdn.com/artworks-Tiwyui2RowYzRxCL-IbJYXQ-t500x500.jpg",
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
        warehouse_stocks = []
        warehouse_id = self.warehouse_ids.attribute_id.mapped('warehouses_id')
        qtyAvailable = self.warehouse_ids.mapped('qtyAvailable')
        for warehouse_id, qtyAvailable in zip(warehouse_id, qtyAvailable):
            warehouse_stocks.append({
                "warehouse_id": warehouse_id,
                "qtyAvailable": qtyAvailable
            })
        # get atributes
        for r in self.attribute_id.mapped('name'):
            data['option_attributes'].append(r)

        if len(data['option_attributes']) == 0:
            data['variants'].append({
                "sku": self.sku,
                "price": self.price,
                "option1": "none",
                "inventory_type": self.inventory_type,
                "warehouse_stocks": warehouse_stocks,
                "image": "https://images-na.ssl-images-amazon.com/images/I/715uwlmCWsLBY.jpg"
            })
        else:
            price = self.attribute_id.value_ids.mapped('price')
            sku = self.attribute_id.value_ids.mapped('sku')
            image = self.attribute_id.value_ids.mapped('image')
            name = self.attribute_id.value_ids.mapped('name')
            if len(data['option_attributes']) == 1:
                for price, sku, image, name in zip(price, sku, image, name):
                    data['variants'].append({
                        "sku": sku,
                        "option1": name,
                        "price": price,
                        "inventory_type": self.inventory_type,
                        "warehouse_stocks": warehouse_stocks,
                        "image": "https://images-na.ssl-images-amazon.com/images/I/715uwlmCWsLBY.jpg",
                    })
            # if len(data['option_attributes']) == 2:
            #     for attribute in self.attribute_id:
            #         price = attribute.value_ids.mapped('price')
            #         sku = attribute.value_ids.mapped('sku')
            #         image = attribute.value_ids.mapped('image')
            #         name = attribute.value_ids.mapped('name')

        payload = json.dumps(data)
        conn.request("POST", "/integration/v2.1/requests", payload, headers)

        res = conn.getresponse().read()
        res_json = json.loads(res.decode("utf-8").replace("'", '"'))
        self.track_id = res_json["track_id"]

        # tracking_tiki = self.env['tracking.tiki']._get_tracking_tiki(self.track_id)
        # tracking_json = json.loads(tracking_tiki.decode("utf-8").replace("'", '"'))
        # self.message_post(
        #     body=f'{self.create_uid.name} -> Trạng thái phê duyệt:  ' + tracking_json['state'] + 'Lý do ' + tracking_json[
        #         'reason'])

    @api.onchange("attribute_id")
    def _check_attribute_id(self):
        if len(self.attribute_id) > 2:
            raise ValidationError("Not more than 2 attribute")
