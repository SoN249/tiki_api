from odoo import fields, models


class ResConfigSettingTiktok(models.TransientModel):
    _inherit = "res.config.settings"

    def btn_sync(self):
        self.env["sale.order"].sync_data_order()
        self.env["stock.picking"].sync_package()
        # self.env['stock.warehouse'].sync_warehouse()
