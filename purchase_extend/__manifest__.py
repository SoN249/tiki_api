{
    'name':"Purchase Extend",
    'sumamary':"Purchase",
    'description':"Long description of module's purpose",
    'category': 'Uncategorized',
    'version': '15.0',
    'depends': ['base','hr','purchase','product'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/s_hr_department.xml',
        'views/s_purchase_order.xml',
        'views/order_limit.xml',
        'views/emloyee_order_limit.xml',
        'wizard/report_department.xml',
        'demo/department_data.xml'
    ],

}