from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class PlanSaleOrder(models.Model):
    _name = 'plan.sale.order'
    _inherit = ['mail.thread']
    _description = "Plan sale order"

    approver = fields.Many2one('res.partner', string='Approver')
    name = fields.Text("Name Plan", required='True')
    quotation = fields.Many2one('sale.order', string="Quotation", readonly="True")
    infor_plan = fields.Text("Infor plan sale", required="True")
    state = fields.Selection(
        [('new', 'New'),
         ('send', 'Send'),
         ('approve', 'Approved'),
         ('refuse', 'Refused'),
         ], string="State", default='new')
    check_send = fields.Boolean(compute='_compute_check_send')
    approver_id = fields.One2many('approver.list', 'plan_sale_order_id', string="Approver")

    def btn_send(self):
        if self.state == 'new' or self.state == 'refuse':
            if self.approver_id.approver:
                self.state = 'send'
                self.approver_id.approval_status = 'not approved yet'
                self.message_post(body=f'{self.create_uid.name} -> The new plan has been sent.',
                                  partner_ids=self.approver_id.approver.ids)
            else:
                raise UserError('Please select approver for plan')
        else:
            raise UserError('The new plan has been sent')

    def _compute_check_send(self):
        current_user_uid = self.env.uid
        for rec in self:
            if rec.create_uid.id == current_user_uid:
                rec.check_send = True
            else:
                rec.check_send = False

    @api.model
    def default_get(self, fields):
        res = super(PlanSaleOrder, self).default_get(fields)
        res['quotation'] = self.env.context.get('active_id')
        return res
