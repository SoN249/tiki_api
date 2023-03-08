from odoo import fields, models

class CategoryTiki(models.Model):
    _name = 'category.tiki'
    name = fields.Char(string='Tên category')
    description = fields.Char(string='Mô tả')
    parent_id = fields.Integer('Parent')
