from odoo import models, fields, api


class SSalesPurchase(models.Model):
    _name = 'sales.purchase'

    def btn_send_email(self):
        # get list id of accountant
        accountant_ids = self.env.ref('purchase_extend.group_staff_accountancy').users
        email_accountant = accountant_ids.mapped('email')

        # get report data of indivicator evaluation
        indicator_evaluation_record = self.env['indicator.evaluation'].search([])

        sales_team_name = indicator_evaluation_record.sale_team.mapped('name')
        real_revenue = indicator_evaluation_record.mapped('real_revenue')
        revenue_difference = indicator_evaluation_record.mapped('revenue_difference')

        # get report data of hr department
        hr_department_record = self.env['hr.department'].search([])
        department_name = hr_department_record.mapped('name')
        department_real_revenue = hr_department_record.mapped('real_revenue')
        department_revenue_defference = hr_department_record.mapped('difference_revenue')

        # data for email templates
        ctx = {'name_department': department_name,
               'department_real_revenue': department_real_revenue,
               'department_revenue_defference': department_revenue_defference,
               'sales_team_name': sales_team_name,
               'real_revenue': real_revenue,
               'revenue_difference': revenue_difference,
               'email_to': ';'.join(map(lambda x: x, email_accountant)),
               'email_from': self.env.user.company_id.email,
               'send_email': True}

        template = self.env.ref('api_report.sale_purchase_email_template')
        template.with_context(ctx).send_mail(self.id, force_send=True, raise_exception=False)
