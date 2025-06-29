# -*- coding: utf-8 -*-
{
    'name': "LMS",

    'summary': "Library Management System for managing books and loans",

    'author': "Menna Reda",
    'version': '17.0.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'mail'],

    # always loaded
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'data/cron_jobs.xml',
        'data/email_template_data.xml',
        'wizards/book_borrow_wizard_view.xml',
        'wizards/book_return_wizard_view.xml',
        'views/library_book_view.xml',
        'views/library_loan_view.xml',
        'views/library_author_view.xml',
        'views/library_dashboard_view.xml',
        'views/actions.xml',
        'reports/report_library_loans_action.xml',
        'views/menu_items.xml',
        'views/res_user_inherit_view.xml',
        'reports/report_library_loans_template.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,

}

