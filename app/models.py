from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), index=True, unique=True)
    description = db.Column(db.String(200))

    def __repr__(self):
        return '<User {0}>'.format(self.name)

    def serialize(self):
        """
        Custom method used within api to serialize database objects into
        JSON.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }
