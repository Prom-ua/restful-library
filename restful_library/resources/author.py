from flask.ext.restful import abort, marshal_with, reqparse
from flask_restful_swagger import swagger

from restful_library import models, db
from restful_library.resources.fields import author_fields, book_fields
from restful_library.resources.base import BaseAuthorBookResource


class BaseAuthorResource(BaseAuthorBookResource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            dest='name',
            type=str,
            required=True,
            help='No author name provided',
        )
        super(BaseAuthorResource, self).__init__()


class AuthorListResource(BaseAuthorResource):

    @swagger.operation(
        notes='Retrieve list of authors',
        responseClass=models.Author.__name__,
    )
    @marshal_with(author_fields)
    def get(self):
        authors = models.Author.query.all()
        return authors

    @swagger.operation(
        notes='Create new author',
        responseClass=models.Author.__name__,
        parameters=[
            {
              'name': 'name',
              'description': "Author's name",
              'dataType': 'string',
              'paramType': 'body',
              'required': True,
              'allowMultiple': False,
            },
        ],
        responseMessages=[
            {
              'code': 201,
              'message': 'Returns created Author'
            },
            {
              'code': 400,
              'message': 'Bad request'
            },
          ]
        )
    @marshal_with(author_fields)
    def post(self):
        args = self.reqparse.parse_args()
        author = models.Author(name=args.name)

        db.session.add(author)
        db.session.commit()
        return author, 201


class AuthorResource(BaseAuthorResource):

    @swagger.operation(
        notes='Retrieve author by id',
        responseClass=models.Author.__name__,
        parameters=[
            {
                'name': 'author_id',
                'dataType': 'string',
                'paramType': 'path',
                'required': True,
            },
        ],
    )
    @marshal_with(author_fields)
    def get(self, author_id):
        return self._get_author(author_id)

    @swagger.operation(
        notes='Update author by id',
        responseClass=models.Author.__name__,
        parameters=[
            {
                'name': 'author_id',
                'dataType': 'string',
                'paramType': 'path',
                'required': True,
            },
            {
              'name': 'name',
              'description': 'Author name',
              'dataType': 'string',
              'paramType': 'body',
              'required': True,
              'allowMultiple': False,
            },
        ],
    )
    @marshal_with(author_fields)
    def put(self, author_id):
        author = self._get_author(author_id)
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                setattr(author, k, v)

        db.session.add(author)
        db.session.commit()
        return author, 201

    @swagger.operation(
        notes='Delete author by id',
        parameters=[
            {
                'name': 'author_id',
                'dataType': 'string',
                'paramType': 'path',
                'required': True,
            },
        ],
    )
    def delete(self, author_id):
        author = self._get_author(author_id)
        db.session.delete(author)
        db.session.commit()
        return '', 204


class AuthorBooksListResource(BaseAuthorResource):

    @swagger.operation(
        notes='Get author books by author id',
        parameters=[
            {
                'name': 'id',
                'dataType': 'string',
                'paramType': 'path',
                'required': True,
            },
        ],
    )
    @marshal_with(book_fields)
    def get(self, id):
        author = self._get_author(id)
        books = (
            models.Book.query
            .filter(models.AuthorsBooks.c.author_id == author.id)
            .join(models.AuthorsBooks)
            .all()
        )
        return books


class AuthorBooksResource(BaseAuthorResource):

    @swagger.operation(
        notes='Add book to author',
        responseClass=models.Book.__name__,
        parameters=[
            {
                'name': 'author_id',
                'dataType': 'string',
                'paramType': 'path',
                'required': True,
            },
            {
                'name': 'book_id',
                'dataType': 'string',
                'paramType': 'path',
                'required': True,
            },
        ],
    )
    @marshal_with(book_fields)
    def put(self, author_id, book_id):
        author = self._get_author(author_id)
        book = self._get_book(book_id)

        author.books.append(book)
        db.session.add(author)
        db.session.commit()
        return author.books, 201

    @swagger.operation(
        notes='Remove book from author',
        parameters=[
            {
                'name': 'author_id',
                'description': 'Author to delete book from',
                'dataType': 'string',
                'paramType': 'path',
                'required': True,
            },
            {
                'name': 'book_id',
                'description': 'Book to remove from author',
                'dataType': 'string',
                'paramType': 'path',
                'required': True,
            },
        ],
    )
    def delete(self, author_id, book_id):
        author = self._get_author(author_id)
        book = self._get_book(book_id)

        if book not in author.books:
            return abort(404, message="Author {} doesn't have book {}".format(
                author_id,
                book_id,
            ))
        author.books.remove(book)
        db.session.add(author)
        db.session.commit()
        return '', 204
