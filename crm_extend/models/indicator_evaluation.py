from odoo import models, fields, api
from odoo.exceptions import ValidationError


class IndicatorEvaluation(models.Model):
    _name = 'indicator.evaluation'

    sale_team = fields.Many2one('crm.team', string='Sale Team', required=True)
    real_revenue = fields.Float(string='Real Revenue', compute='_compute_real_revenue', store=False)
    month = fields.Selection([
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December')
    ], required="True")
    month_revenue = fields.Float('Month Revenue', compute='_compute_month_revenue', store=True)
    create_month = fields.Integer('Create Month', compute='_compute_create_month', store=True)

    # Calculate real_revenue = amount_untaxed corresponding to the opportunity
    def _compute_real_revenue(self):
        for rec in self:
            if rec.sale_team:
                amount_untaxed_opportunity = self.env['sale.order'].search(
                    [('team_id', 'in', rec.sale_team.mapped('id')), ('opportunity_id', '!=', False),('state','=','sale')])
                rec.real_revenue = sum(amount_untaxed_opportunity.mapped('amount_untaxed'))

    # Get value month revenue to month of report
    @api.depends('month')
    def _compute_month_revenue(self):
        for rec in self:
            if rec.sale_team:
                month_sales_result = self.env['crm.team'].search([('id', '=', rec.sale_team.mapped('id'))])

                month_sales = month_sales_result.mapped(lambda res: (res.January, res.February, res.March, res.April,
                                                                     res.May, res.June, res.July, res.August,
                                                                     res.September,
                                                                     res.October, res.November, res.December))
                rec.month_revenue = month_sales[0][int(rec.month) - 1]

    def _compute_create_month(self):
        for rec in self:
            if rec.create_date:
                rec.create_month = rec.create_date.month
