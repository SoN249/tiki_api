from odoo import fields, models, api


class SSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    confirmation = fields.Selection([('waiting', 'Chờ người bán xác nhận'),
                                     ('seller_confirmed', 'Xác nhận có hàng'),
                                     ('seller_canceled', 'Xác nhận không có hàng'),
                                     ('confirmed', 'Đã xác nhận'),
                                     ('ready_to_pick', 'Hàng chuẩn bị vận chuyển')
                                     ], string="Trạng thái xác nhận")
    fee = fields.Float("Phí sản phẩm")
