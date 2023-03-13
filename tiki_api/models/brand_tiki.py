from odoo import fields, models
import http.client
import json
class BrandTiki(models.Model):
    _name = 'brand.tiki'
    name = fields.Char(string='Tên thương hiệu')