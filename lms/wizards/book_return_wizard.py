from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ReturnBookWizard(models.TransientModel):
    _name = 'library.book.return.wizard'
    _description = 'Return Book Wizard'
    loan_id = fields.Many2one(
        'library.loan',
        string='Loan',
        required=True,
        readonly=True,
        help="The loan record from which the book is being returned."
    )
    loan_line_ids = fields.Many2many('library.loan.line', string='Loan_line', required=True, readonly=True)


    @api.model
    def default_get(self, fields_list):
        res = super(ReturnBookWizard, self).default_get(fields_list)
        active_id = self.env.context.get('active_id')
        if active_id:
            loan = self.env['library.loan'].browse(active_id)
            available_loan_lines = loan.loan_line_ids.filtered(lambda l: l.status != 'returned')
            if not available_loan_lines:
                raise ValidationError("All books for this loan have already been returned or there are no active loan lines.")
            res['loan_id'] = active_id
            res['loan_line_ids'] = [(6, 0, available_loan_lines.ids)]
        return res


    def action_return_books(self):
        self.ensure_one()
        if not self.loan_line_ids:
            raise ValidationError("Please select at least one book to return.")
        for line in self.loan_line_ids:
            if line.status != 'returned':
                line.status = 'returned'

        return {
            'type': 'ir.actions.act_window_close',
            'effect': {
                'fadeout': 'slow',
                'message': f'{len(self.loan_line_ids)} book(s) have been successfully marked as returned.',
                'type': 'rainbow_man',
            }
        }






