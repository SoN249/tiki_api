from odoo import api, models, fields
from odoo.exceptions import UserError


class AproverList(models.Model):
    _name = "approver.list"
    _description = "Approver List"

    approver = fields.Many2one('res.partner', string='Approver')
    approval_status = fields.Selection([
        ('not approved yet', 'Not Approved Yet'),
        ('approve', 'Approved'),
        ('refuse', 'Refused'),
    ], string='Approval Status', default='not approved yet', readonly=True)
    plan_sale_order_id = fields.Many2one('plan.sale.order', string='Plan Sale Order')
    check_approver = fields.Boolean(compute='_compute_check_approver')

    def _compute_check_approver(self):
        # get id approve currently
        approver_current = self.env.user.partner_id.id

        # get list of approve
        approver_list = self.plan_sale_order_id.approver_id.approver

        # Check approve current in approve list
        if approver_current in approver_list.ids and self.plan_sale_order_id.state == 'send':
            self.check_approver = True
        else:
            self.check_approver = False

    def btn_approve(self):
        # Get approver of plan sales order
        approver = self.approver

        # Get id of approver current
        approver_current = self.env.user.partner_id

        # Check approve in plan sales order
        if approver_current == approver:
            self.approval_status = 'approve'
            approver_id = self.plan_sale_order_id.approver_id
            list_status = approver_id.mapped('approval_status')
            # Check all status of plan is approved then plan is approve
            if all(x == 'approve' for x in list_status):
                self.plan_sale_order_id.state = 'approve'
                self.plan_sale_order_id.message_post(
                    body=f'{self.env.user.name}-> {self.plan_sale_order_id.name} plan has been approved.',
                    partner_ids=self.plan_sale_order_id.create_uid.partner_id.ids)
        else:
            raise UserError("This is not allowed approve")

    def btn_refuse(self):
        approver = self.approver
        approver_current = self.env.user.partner_id
        if approver_current == approver:
            self.approval_status = 'refuse'
            self.plan_sale_order_id.state = 'refuse'
            self.plan_sale_order_id.message_post(
                    body=f'{self.env.user.name}-> {self.plan_sale_order_id.name} plan has been refused.',
                    partner_ids=self.plan_sale_order_id.create_uid.partner_id.ids)

        else:
            raise UserError("This is not allowed approve")
