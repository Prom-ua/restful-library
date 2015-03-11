from restful_library import db


AuthorsBooks = db.Table(
    'authors_books',
    db.Column('author_id', db.Integer, db.ForeignKey('author.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Author %r>' % (self.id)

    def __unicode__(self):
        return '%s' % (self.name)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    authors = db.relationship(
        'Author',
        secondary=AuthorsBooks,
        backref='books',
    )

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Book %r>' % (self.id)

    def __unicode__(self):
        return '%s' % (self.title)
