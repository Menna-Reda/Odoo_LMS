from odoo import models, fields, api

class ResUserInherit(models.Model):
    _inherit = 'res.users'
    is_library_member = fields.Boolean(string='Is library member')
    loan_ids = fields.Many2many('library.loan', string='Loans')
    loan_count = fields.Integer(compute='_compute_loan_count', string='Loan count')
    email = fields.Char(
        compute='_compute_email_from_login',
        store=True,
        string="Email Address (Synchronized)"
    )

    def _compute_loan_count(self):
        for loan in self:
            loan.loan_count = len(loan.loan_ids)

    @api.depends('login')
    def _compute_email_from_login(self):
        """
        Computes the 'email' field value from the 'login' field.
        """
        for user in self:
            user.email = user.login

