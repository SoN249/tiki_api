from odoo import fields, models

class BrandTiki(models.Model):
    _name = 'brand.tiki'
    name = fields.Char(string='Tên thương hiệu')