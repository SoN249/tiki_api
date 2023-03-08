from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class SHrDepartment(models.Model):
    _inherit = 'hr.department'
    _description = 'Manage department'
    limit = fields.Float('Spending limit', digits=(12, 2))
    real_revenue = fields.Float(string='Real Revenue', compute='_compute_real_revenue', store=False)
    create_month = fields.Integer('Create Month', compute='_compute_create_month', store=True)

    @api.onchange('limit')
    def _check_spending_limit(self):
        if self.limit:
            if self.limit < 0:
                raise ValidationError("Value expected must be valid positive")

    # Calculate real_revenue = amount_total corresponding to the department
    def _compute_real_revenue(self):
        for rec in self:
            if rec.name:
                amount_total = self.env['purchase.order'].search([('department', '=', rec.id)])
                amount_total_department = amount_total.mapped('amount_total')
                rec.real_revenue = sum(amount_total_department)


    def _compute_create_month(self):
        for rec in self:
            if rec.create_date:
                rec.create_month = rec.create_date.month
