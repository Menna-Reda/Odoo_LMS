from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
class LibraryLoanLine(models.Model):
    _name = 'library.loan.line'
    _description = 'Library Loan Line'
    _rec_name = 'book_id'
    book_id = fields.Many2one('library.book', string='Book')
    loan_id = fields.Many2one('library.loan', string='Loan')
    status = fields.Selection([('active', 'Active'),('returned', 'Returned'),('overdue','Overdue')], string='status', default='active')

    @api.constrains('status', 'book_id')
    def _validate_available_copies(self):
        for line in self:
            if line.status == 'active' and line.book_id and line.book_id.available_copies < 0:
                raise ValidationError(f"Cannot borrow '{line.book_id.title}': no available copies.")

    def action_return_book(self):
        for line in self:
            line.status = 'returned'






