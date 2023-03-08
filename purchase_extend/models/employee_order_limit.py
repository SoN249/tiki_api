from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError


class EmployeeOrderLimit(models.Model):
    _name = 'employee.order.limit'
    employee = fields.Many2one('res.users', string="Employee Order limit", required=True)
    order_limit = fields.Float(string='Order Limit', digits=(14, 2))

    @api.onchange('order_limit')
    def _check_order_limit(self):
        for r in self:
            if r.order_limit < 0:
                raise ValidationError("Value expected must be valid positive")
