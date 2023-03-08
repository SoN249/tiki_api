from odoo import api, models, fields
from datetime import date


class SIndicatorEvaluation(models.Model):
    _inherit = 'indicator.evaluation'

    revenue_difference = fields.Float('Revenue Difference', compute='_compute_revenue_difference')

    def _compute_revenue_difference(self):
        current_month = date.today().month
        for rec in self:
            if rec.real_revenue:
                # calculate revenue difference
                month_sales_result = self.env['crm.team'].search([('id', 'in', rec.sale_team.ids)])
                month_sales = month_sales_result.mapped(lambda res: (res.January, res.February, res.March, res.April,
                                                                     res.May, res.June, res.July, res.August,
                                                                     res.September,
                                                                     res.October, res.November, res.December))

                rec.revenue_difference = rec.real_revenue - month_sales[0][current_month - 1]
            else:
                rec.revenue_difference = 0
