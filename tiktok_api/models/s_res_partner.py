from odoo import fields, models


class SResPartner(models.Model):
    _inherit = "res.partner"

    is_tiktok_customer = fields.Boolean('Is tiktok')