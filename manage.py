from flask.ext.script import Shell
from flask.ext.migrate import MigrateCommand

from restful_library import app
from restful_library import db
from restful_library import manager


def _make_context():
    return dict(app=app, db=db)

manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
