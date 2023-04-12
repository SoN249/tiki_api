from odoo import fields, models


class ResConfigSettingTiktok(models.TransientModel):
    _inherit = "res.config.settings"

    def btn_sync(self):
        customer_tiktok={
            "name": "TMĐT-Tiktok customer",
            "is_tiktok_customer": True,
            "street": "Tiktok customer",
            "city": "Tiktok customer",
        }
        self.env['res.partner'].sudo().create(customer_tiktok)
        self.env['stock.warehouse'].sync_warehouse()
        self.env['sale.order'].sync_data_order()
        self.env['stock.picking'].sync_package()