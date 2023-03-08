from odoo import models, fields


class OrderLimit(models.Model):
    _name = 'order.limit'
    name = fields.Char("Limit")
    employee_order_limit = fields.Many2many('employee.order.limit', string="Employee order limit")