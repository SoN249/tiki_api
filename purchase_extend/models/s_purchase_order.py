from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError


class SPurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    department = fields.Many2one('hr.department', string="Department", required="True")

    def button_confirm(self):
        # get role of users
        desired_group_name = self.env.ref('purchase_extend.group_staff_accountancy')
        is_desired_group = self.env.user.id in desired_group_name.users.ids

        # get list order limit of employee
        current_user_id = self.env.uid
        employee_line = self.env['employee.order.limit'].search([('employee', '=', current_user_id)],
                                                                order='order_limit DESC')
        employee_limit = employee_line.mapped('order_limit')

        for rec in self:
            if rec.amount_total and employee_limit:
                # Check order limit of employee and amount total
                if rec.amount_total < employee_limit[0]:
                    return super(SPurchaseOrder, self).button_confirm()
                else:
                    if is_desired_group == False:
                        raise ValidationError('The total request exceeds the limit. Please send it to the accountant.')
                    else:
                        return super(SPurchaseOrder, self).button_confirm()
            else:
                if is_desired_group == False:
                    raise ValidationError('You can not confirm order because you unlimited. '
                                          'Please send it to the accountant')
                else:
                    return super(SPurchaseOrder, self).button_confirm()
