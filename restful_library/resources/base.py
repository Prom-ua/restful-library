from flask.ext import restful

from restful_library import models
from restful_library.lib.auth import token_authenticate


class Resource(restful.Resource):
    method_decorators = [token_authenticate]


class BaseAuthorBookResource(Resource):

    def _get_book(self, book_id):
        book = models.Book.query.get(book_id)
        if not book:
            restful.abort(404, message="Book {} doesn't exist".format(book_id))
        return book

    def _get_author(self, author_id):
        author = models.Author.query.get(author_id)
        if not author:
            restful.abort(404, message="Author {} doesn't exist".format(
                author_id,
            ))
        return author
