from odoo import models, api, fields
from odoo.exceptions import UserError, ValidationError

class SCrmTeam(models.Model):
    _inherit = "crm.team"
    _description = "Crm sales team"

    currency_id = fields.Many2one('res.currency', string='Currency', readonly= False, store= True, required=True)
    January = fields.Float('January')
    February = fields.Float('February')
    March = fields.Float('March')
    April = fields.Float('April')
    May = fields.Float('May')
    June = fields.Float('June')
    July = fields.Float('July')
    August = fields.Float('August')
    September = fields.Float('September')
    October = fields.Float('October')
    November = fields.Float('November')
    December = fields.Float('December')

    @api.onchange('January','February','March','April','May','June','July','August','September','October','November','December')
    def check_month_value(self):
        for r in self:
            #Check value of month target
            if r.January < 0 or r.February < 0 or r.March < 0 or r.April < 0 or r.May < 0 or r.June < 0 or r.July < 0 or r.August < 0 or r.September < 0 or r.October < 0 or r.November < 0 or r.December < 0:
                raise ValidationError('Value expected must be valid positive')

