# -*- coding:utf-8 -*-
import os
from app import create_app, db
from app.web.models import Table, Aspect, Universum, Dimension
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db,
                Table=Table,
                Aspect=Aspect,
                Universum=Universum,
                Dimension=Dimension)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()