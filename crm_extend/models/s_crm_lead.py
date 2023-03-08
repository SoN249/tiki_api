from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError


class SCrmLead(models.Model):
    _inherit = "crm.lead"
    _description = "Manager CRM"

    revenue = fields.Float("Doanh thu tối thiểu (trước VAT)")
    real_revenue = fields.Float(string='Doan thu thực tế', compute='_compute_real_revenue', store=False)
    create_month = fields.Integer('Create Month', compute='_compute_create_month', store=True)
    sale_team = fields.Many2many('crm.team', string="Sale team")


    def _get_user_id(self):

        team_id = self.env.user.sale_team_id.ids
        sales_staff_in_group = self.env['crm.team.member'].search([('crm_team_id', 'in', team_id)]).user_id.ids
        #
        get_team = self.env['crm.team'].search([('user_id', '=', self.env.uid)])
        get_member_team = self.env['crm.team.member'].search([('crm_team_id', 'in', get_team.ids)]).user_id.ids

        get_leader_id = get_team.user_id.ids

        if get_team:
            return ['|', ('id', '=', get_leader_id), ('id', '=', get_member_team)]
        else:
            return [('id', 'in', sales_staff_in_group)]

    user_id = fields.Many2one(
        'res.users', string='Salesperson', default=lambda self: self.env.user,
        domain="['&', ('share', '=', False), ('company_ids', 'in', user_company_ids)]" and _get_user_id,
        check_company=True, index=True, tracking=True)

    @api.onchange('revenue')
    def _check_min_revenue(self):
        for r in self:
            if r.revenue < 0:
                raise ValidationError("Value expected must be valid positive")

    def _compute_real_revenue(self):
        for rec in self:
            if rec.id:
                amount_total = self.env['sale.order'].search([('opportunity_id', '=', rec.id)])
                rec.real_revenue = sum(amount_total.mapped('amount_total'))

    @api.depends('create_date')
    def _compute_create_month(self):
        for rec in self:
            if rec.create_date:
                rec.create_month = rec.create_date.month

    def action_set_lost(self, **additional_values):
        # Check role of user current is Leader
        desired_group_name = self.env.ref('crm_extend.group_staff_leader')
        is_desired_group = self.env.user.id in desired_group_name.users.ids

        for rec in self:
            if rec.priority == '3':
                if is_desired_group == True:
                    return super(SCrmLead, self).action_set_lost()
                else:
                    raise UserError("You not allowed mark lost")
            else:
                return super(SCrmLead, self).action_set_lost()
