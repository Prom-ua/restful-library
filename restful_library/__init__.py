from flask import Flask
from flask.ext import restful
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')

api = restful.Api(app)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите, чтобы получить доступ к этой странице.'
login_manager.login_message_category = 'info'


from restful_library import models, views


from restful_library.resources.book import (
    BookListResource,
    BookResource,
    BookAuthorsListResource,
    BooksAuthorsResource,
)
api.add_resource(BookListResource, '/books/')
api.add_resource(BookResource, '/books/<book_id>/')
api.add_resource(
    BookAuthorsListResource,
    '/books/<id>/authors/',
    endpoint='book_authors_list',
)
api.add_resource(
    BooksAuthorsResource,
    '/books/<book_id>/authors/<author_id>/',
    endpoint='book_authors',
)


from restful_library.resources.author import (
    AuthorListResource,
    AuthorResource,
    AuthorBooksListResource,
    AuthorBooksResource,
)
api.add_resource(AuthorListResource, '/authors/')
api.add_resource(AuthorResource, '/authors/<author_id>/')
api.add_resource(
    AuthorBooksListResource,
    '/authors/<id>/books/',
    endpoint='author_books_list',
)
api.add_resource(
    AuthorBooksResource,
    '/authors/<author_id>/books/<book_id>/',
    endpoint='author_books',
)
