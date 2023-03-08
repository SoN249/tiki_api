from odoo import fields, models

class ProductTiki(models.Model):
    _name = 'product.tiki'

    name = fields.Char(string="Tên sản phẩm")
    description = fields.Html('Mô tả')
    category_id = fields.Many2one('category.tiki', string="Danh mục")
    brand_id = fields.Many2one('brand.tiki', string='Thương hiệu' )
    brand_country = fields.Char(string="Xuất xứ thương hiệu")
    origin = fields.Char(string="Xuất xứ")
    product_height = fields.Float(string="Chiều cao")
    product_width = fields.Float(string="Chiều rộng")
    product_length = fields.Float(string="Chiều dài")
    is_warranty_applied = fields.Boolean('Warranty')
    option_attributes = fields.Char(string="Thuộc tính lựa chọn")
    image = fields.Image(string="Ảnh sản phẩm")
    sku = fields.Char(string="Mã sản phẩm")
    price = fields.Float("Giá sản phẩm")
    option1 = fields.Char(string="Thuộc tính")
    inventory_type = fields.Selection([('1', 'dropship'),
                                       ('2', 'instock')
                                       ])
    warehouse_id = fields.Many2one('warehauses.tiki',string="Kho")
    is_auto_turn_on = fields.Boolean('Is auto turn on')