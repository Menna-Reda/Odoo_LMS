from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class BookBorrowWizard(models.TransientModel):
    _name = 'library.book.borrow.wizard'
    _description = 'Book Borrow Wizard'

    book_id = fields.Many2one('library.book',string='Book',required=True,readonly=True)
    partner_id = fields.Many2one('res.users',string='Borrower',required=True,help="Select the partner who is borrowing this book. Only individuals are shown.")
    borrow_date = fields.Date(string='Borrow Date',default=fields.Date.context_today,required=True,help="The date when the book is borrowed.")

    @api.model
    def default_get(self, fields_list):
        """
        Overrides the default_get method to pre-fill the book_id based on the active_id
        from the context (i.e., the book record from which the wizard was opened).
        It also validates if the selected book is available for borrowing.
        """
        res = super().default_get(fields_list)
        active_id = self.env.context.get('active_id')  # Get the ID of the current book record

        if active_id:
            book = self.env['library.book'].browse(active_id)
            if book.available_copies > 0:
                res['book_id'] = active_id
            else:
                raise ValidationError(
                    f"The book '{book.title}' is currently not available for borrowing.")
        return res

    def action_borrow_book(self):
        """
        This method is called when the "Borrow Book" button in the wizard is clicked.
        It creates a new 'library.loan' record and a corresponding 'library.loan.line'
        to register the borrowing of the selected book by the chosen partner.
        """
        self.ensure_one()
        # Re-check available copies to prevent concurrent borrowing issues
        if self.book_id.available_copies <= 0:
            raise ValidationError(f"Cannot borrow '{self.book_id.title}': no available copies.")
        loan = self.env['library.loan'].create({
            'partner_id': self.partner_id.id,
            'borrow_date': self.borrow_date,})

        self.env['library.loan.line'].create({
            'loan_id': loan.id,
            'book_id': self.book_id.id,
            'status': 'active',
        })

        return {
            'name': 'New Book Loan',
            'type': 'ir.actions.act_window',
            'res_model': 'library.loan',
            'view_mode': 'form',
            'res_id': loan.id,
            'target': 'current',
            'flags': {'new_window': True}  # Opens in a new full window/tab, rather than dialog
        }
