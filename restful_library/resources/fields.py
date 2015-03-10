from flask.ext.restful import fields


author_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'books': fields.Url('author_books_list')
}

book_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'authors': fields.Url('book_authors_list'),
}
