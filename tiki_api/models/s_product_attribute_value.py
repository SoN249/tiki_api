from odoo import fields, models


class SProductAttributeValue(models.Model):
        _inherit = "product.attribute.value"

        price = fields.Float('Giá bán')
        sku = fields.Char(string='Mã sản phẩm ')
        # image = fields.Image(string='Ảnh đại diện')
        image = fields.Char(string='Ảnh đại diện')