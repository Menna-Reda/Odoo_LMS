from odoo import api, fields, models
from odoo.exceptions import ValidationError

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Book in the library'
    _rec_name = 'title'
    title = fields.Char(string='Book title', required=True)
    author_id = fields.Many2one('library.author', string='Author', required=True)
    isbn = fields.Char(string='ISBN', required=True, size=13, help="International Standard Book Number (13 digits)")
    publication_year = fields.Integer(string='Publication year')
    loan_line_ids = fields.One2many('library.loan.line', 'book_id', string='Loan lines')
    status = fields.Selection([
        ('available', 'Available'),
        ('borrowed', 'Borrowed')
    ], default='available')
    total_copies = fields.Integer(string='Total copies', default=1, required=True)
    available_copies = fields.Integer(string='Available copies', compute='_compute_available_copies')
    

    _sql_constraints = [
        ('isbn_unique', 'UNIQUE(isbn)', 'Book ISBN must be unique')
    ]

    @api.constrains('isbn')
    def _check_isbn(self):
        for book in self:
            if not book.isbn or len(book.isbn) != 13 or not book.isbn.isdigit():
                raise ValidationError("ISBN must be exactly 13 numeric digits.")

    @api.depends('loan_line_ids.status')
    def _compute_available_copies(self):
        for book in self:
            borrowed_lines = book.loan_line_ids.filtered(lambda l: l.status != 'returned' and l.loan_id.status == 'borrowed')
            book.available_copies = book.total_copies - len(borrowed_lines)

    @api.depends('available_copies')
    def _compute_status(self):
        for book in self:
            book.status = 'borrowed' if book.available_copies <= 0 else 'available'

    @api.constrains('total_copies')
    def _check_total_copies_positive(self):
        for book in self:
            if book.total_copies < 0:
                raise ValidationError("Total copies cannot be negative.")

    @api.constrains('available_copies')
    def _check_available_copies_positive(self):
        for book in self:
            if book.available_copies < 0:
                book.available_copies = 0
                raise ValidationError("Available_copies copies cannot be negative.")