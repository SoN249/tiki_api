from odoo import api, models, fields


class SPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    vendors = fields.Char('Vendor Suggest', compute='_compute_vendor', store=True)
    product_id = fields.Many2one('product.product', string='Product', domain=[('purchase_ok', '=', True)],
                                 change_default=True, index='btree_not_null')

    @api.depends('product_id')
    def _compute_vendor(self):
        for rec in self:
            if rec.product_id:
                supplier_line_delay = self.env['product.supplierinfo'].search([('product_id', '=', rec.product_id.id)],
                                                                              order='delay asc')
                if supplier_line_delay:
                    supplier_line_price = supplier_line_delay.sorted(lambda x: x.price)
                    supplier_name = supplier_line_price.mapped('partner_id.name')[0]
                    rec.vendors = supplier_name
                else:
                    rec.vendors = ''
