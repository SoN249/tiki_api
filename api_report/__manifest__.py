{
    'name': "Api Report",
    'summary': "My api",
    'depends': ['base','crm_extend','purchase_extend','mail','hr'],
    'version': '15.0.1',
    'data': [
        'security/ir.model.access.csv',
        'views/ss_hr_department.xml',
        'views/s_indicator_evaluation.xml',
        'views/s_sales_purchase.xml',
        'data/sale_purchase_email_template.xml',
        'data/scheduled_action.xml'
    ]
}