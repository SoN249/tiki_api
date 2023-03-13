from odoo import fields, models


class ProductOrigin(models.Model):
    _name= "product.origin"
    name = fields.Char(string="Tên quốc gia")