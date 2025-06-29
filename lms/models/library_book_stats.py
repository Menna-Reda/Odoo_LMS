from odoo import api, fields, models, _, tools

class LibraryBookStats(models.Model):
    _name = 'library.book.stats'
    _description = 'Top Borrowed Books (SQL View)'
    _auto = False
    book_id = fields.Many2one('library.book', string='Book', readonly=True)
    borrow_count = fields.Integer(string='Borrow Count', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute('''
        CREATE OR REPLACE VIEW library_book_stats AS (
        SELECT MIN(id) as id, book_id, COUNT(*) as borrow_count
        FROM library_loan_line
        GROUP BY book_id
        ORDER BY borrow_count DESC
        LIMIT 3)    
                     ''')