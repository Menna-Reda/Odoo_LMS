from odoo import api, fields, models


class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Book Author'

    name = fields.Char(required=True)
    bio = fields.Text()
    birth_date = fields.Date()
