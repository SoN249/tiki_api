{
    'name': "CRM Extend",
    'summary': "Manage my crm",
    'depends': ['base','crm','sale','sale_crm'],
    'version': '15.0.1',
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/s_crm_lead.xml',
        'views/s_crm_team.xml',
        'views/s_sale_order.xml',
        'views/plan_sales_order.xml',
        'views/indicator_evaluation.xml',
        'wizard/report_detail.xml',
        'wizard/report_indicator_evaluation.xml',
    ]
}