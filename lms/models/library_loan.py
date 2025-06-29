from odoo import models, fields, api
from datetime import timedelta, date
import logging
_logger = logging.getLogger(__name__)

class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Books loans for library members'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.users', string='Partner', required=True)
    borrow_date = fields.Date(string='Borrow Date', default=fields.Date.context_today)
    return_date = fields.Date(string='Return Date', compute="_compute_return_date", store=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue')
    ], string='Status', compute='_compute_status', store=True, default='draft')

    manual_status_override = fields.Selection([
        ('draft', 'Draft'),
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ], string='Manual Override', tracking=True)

    loan_line_ids = fields.One2many('library.loan.line', 'loan_id', string='Loan Lines',required=True)
    book_ids = fields.Many2many(
        'library.book',
        compute='_compute_book_ids',
        string='Books in Loan',
        store=False
    )

    @api.depends('loan_line_ids.book_id')
    def _compute_book_ids(self):
        for loan in self:
            loan.book_ids = loan.loan_line_ids.mapped('book_id')

    @ api.depends('borrow_date')
    def _compute_return_date(self):
        for loan in self:
            if loan.borrow_date:
                loan.return_date = (loan.borrow_date + timedelta(days=14))

    @api.depends('manual_status_override', 'loan_line_ids.status')
    def _compute_status(self):
        for loan in self:
            if loan.manual_status_override:
                loan.status = loan.manual_status_override
                loan.manual_status_override = False
            else:
                statuses = loan.loan_line_ids.mapped('status')
                if not statuses:
                    loan.status = 'draft'
                elif all(s == 'returned' for s in statuses):
                    loan.status = 'returned'
                elif any(s == 'overdue' for s in statuses):
                    loan.status = 'overdue'
                elif all(s == 'active' for s in statuses):
                    loan.status = 'borrowed'
                else:
                    loan.status = 'draft'

    def send_email(self):
        template = self.env.ref('lms.overdue_loans_reminder_mail_template')
        for loan in self:
            template.send_mail(loan.id, force_send=True)


    def update_overdue_loans(self):
        overdue_loans = self.search([
            ('status', '!=', 'returned'),
            ('status', '!=', 'overdue'),
            ('status', '!=', 'draft'),
            ('return_date', '<', date.today()),
        ])
        for loan in overdue_loans:
            loan.status = 'overdue'
            for loan_line in loan.loan_line_ids:
                if loan_line.status != 'returned':
                    loan_line.status = 'overdue'
            loan.send_email()
            _logger.info(f"Marked loan #{loan.id} as overdue.")

    def action_reset_to_draft(self):
        for loan in self:
            for line in loan.loan_line_ids:
                line.status = 'active'
            loan.manual_status_override = 'draft'

    def action_borrow(self):
        for loan in self:
            for line in loan.loan_line_ids:
                line.status = 'active'
            loan.manual_status_override = 'borrowed'



