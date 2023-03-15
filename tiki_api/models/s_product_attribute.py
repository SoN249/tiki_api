from odoo import fields, models



class SProductAttribute(models.Model):
    _inherit = 'product.attribute'

    product_id = fields.Many2one('product.product')




