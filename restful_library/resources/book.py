from flask.ext.restful import abort, marshal_with, reqparse
from flask_restful_swagger import swagger

from restful_library import models, db
from restful_library.resources.fields import author_fields, book_fields
from restful_library.resources.base import BaseAuthorBookResource


class BaseBookResource(BaseAuthorBookResource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title',
            dest='title',
            type=str,
            required=True,
            help='No book title provided',
        )
        super(BaseBookResource, self).__init__()


class BookListResource(BaseBookResource):

    @swagger.operation(
        notes='Retrieve list of books',
        responseClass=models.Book.__name__,
    )
    @marshal_with(book_fields)
    def get(self):
        books = models.Book.query.all()
        return books

    @swagger.operation(
        notes='Create new book',
        responseClass=models.Book.__name__,
        parameters=[
            {
              'name': 'title',
              'description': "Books's name",
              'dataType': 'string',
              'paramType': 'body',
              'required': True,
              'allowMultiple': False,
            },
          ],
        responseMessages=[
            {
              'code': 201,
              'message': 'Returns created Book'
            },
            {
              'code': 400,
              'message': 'Bad request'
            },
          ]
        )
    @marshal_with(book_fields)
    def post(self):
        args = self.reqparse.parse_args()
        book = models.Book(title=args.title)

        db.session.add(book)
        db.session.commit()
        return book, 201


class BookResource(BaseBookResource):

    @swagger.operation(
        notes='Retrieve book by id',
        responseClass=models.Book.__name__,
        parameters=[
            {
                'name': 'book_id',
                'dataType': 'string',
                'paramType': 'path',
                'required': True,
            },
        ],
    )
    @marshal_with(book_fields)
    def get(self, book_id):
        return self._get_book(book_id)

    @swagger.operation(
        notes='Update book by id',
        responseClass=models.Book.__name__,
        parameters=[
            {
                'name': 'book_id',
                'dataType': 'string',
                'paramType': 'path',
                'required': True,
            },
            {
              'name': 'title',
              'description': 'Book name',
              'dataType': 'string',
              'paramType': 'body',
              'required': True,
              'allowMultiple': False,
            },
        ],
    )
    @marshal_with(book_fields)
    def put(self, book_id):
        book = self._get_book(book_id)
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                setattr(book, k, v)

        db.session.add(book)
        db.session.commit()
        return book, 201

    @swagger.operation(
        notes='Delete book by id',
        parameters=[
            {
                'name': 'book_id',
                'dataType': 'string',
                'paramType': 'path',
                'required': True,
            },
        ],
    )
    def delete(self, book_id):
        book = self._get_book(book_id)
        db.session.delete(book)
        db.session.commit()
        return '', 204


class BookAuthorsListResource(BaseBookResource):

    @swagger.operation(
        notes='Get book authors by book id',
        parameters=[
            {
                'name': 'id',
                'dataType': 'string',
                'paramType': 'path',
                'required': True,
            },
        ],
    )
    @marshal_with(author_fields)
    def get(self, id):
        book = self._get_book(id)
        authors = (
            models.Author.query
            .filter(models.AuthorsBooks.c.book_id == book.id)
            .join(models.AuthorsBooks)
            .all()
        )
        return authors


class BooksAuthorsResource(BaseBookResource):

    @swagger.operation(
        notes='Add author to book',
        responseClass=models.Author.__name__,
        parameters=[
            {
                'name': 'book_id',
                'dataType': 'string',
                'paramType': 'path',
                'required': True,
            },
            {
                'name': 'author_id',
                'dataType': 'string',
                'paramType': 'path',
                'required': True,
            },
        ],
    )
    @marshal_with(author_fields)
    def put(self, book_id, author_id):
        book = self._get_book(book_id)
        author = self._get_author(author_id)

        book.authors.append(author)
        db.session.add(book)
        db.session.commit()
        return book.authors, 201

    @swagger.operation(
        notes='Remove author from book',
        parameters=[
            {
                'name': 'book_id',
                'description': 'Book to delete author from',
                'dataType': 'string',
                'paramType': 'path',
                'required': True,
            },
            {
                'name': 'author_id',
                'description': 'Author to remove from book',
                'dataType': 'string',
                'paramType': 'path',
                'required': True,
            },
        ],
    )
    def delete(self, book_id, author_id):
        book = self._get_book(book_id)
        author = self._get_author(author_id)

        if author not in book.authors:
            return abort(404, message="Book {} doesn't have author {}".format(
                book_id,
                author_id,
            ))
        book.authors.remove(author)
        db.session.add(book)
        db.session.commit()
        return '', 204
