#!/usr/bin/env python

# model import is required to set up database correctly
from app.models import db, User
from app import create_app
from config import base


app = create_app(base, db)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # creates user if one doesn't exist
        if User.query.filter_by(name='user') is None:
            usr = User(name='user', description='')
            db.session.add(usr)
            db.session.commit()

    app.run()
