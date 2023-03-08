from odoo import models, fields, api


class SSHrDepartment(models.Model):
    _inherit = 'hr.department'

    difference_revenue = fields.Float('Difference Revenue', compute='_compute_difference_revenue', store=False)

    def _compute_difference_revenue(self):
        for rec in self:
            if rec.real_revenue:
                rec.difference_revenue = rec.real_revenue - rec.limit
            else:
                rec.difference_revenue = 0
