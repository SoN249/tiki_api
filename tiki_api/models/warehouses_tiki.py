from odoo import fields, models

class WerehousesTiki(models.Model):
    _name = 'warehauses.tiki'
    name = fields.Char(string='Tên category')
    code = fields.Char(string='Code')