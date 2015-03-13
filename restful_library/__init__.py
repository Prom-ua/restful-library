from flask import Flask
from flask.ext import restful
from flask.ext.login import LoginManager
from flask.ext.migrate import Migrate
from flask.ext.restful.utils import cors
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful_swagger import swagger


app = Flask(__name__)
app.config.from_object('config')

api = swagger.docs(
    restful.Api(
        app,
        decorators=[
            cors.crossdomain(origin='*', headers='Authorization'),
        ],
    ),
    apiVersion='0.1',
    api_spec_url='/spec',
)
api_prefix_url = '/api/v1'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)

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


# Temporary solution to add prefix due to bug in Flask-Restful-Swagger
# with static html content (spec.html)

api.add_resource(BookListResource, api_prefix_url + '/books')
api.add_resource(BookResource, api_prefix_url + '/books/<int:book_id>')
api.add_resource(
    BookAuthorsListResource,
    api_prefix_url + '/books/<int:id>/authors',
    endpoint='book_authors_list',
)
api.add_resource(
    BooksAuthorsResource,
    api_prefix_url + '/books/<int:book_id>/authors/<int:author_id>',
    endpoint='book_authors',
)


from restful_library.resources.author import (
    AuthorListResource,
    AuthorResource,
    AuthorBooksListResource,
    AuthorBooksResource,
)
api.add_resource(AuthorListResource, api_prefix_url + '/authors')
api.add_resource(AuthorResource, api_prefix_url + '/authors/<int:author_id>')
api.add_resource(
    AuthorBooksListResource,
    api_prefix_url + '/authors/<int:id>/books',
    endpoint='author_books_list',
)
api.add_resource(
    AuthorBooksResource,
    api_prefix_url + '/authors/<int:author_id>/books/<int:book_id>',
    endpoint='author_books',
)
