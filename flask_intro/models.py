from .app import db


class Country(db.Model):
    """Model for storing countries"""
    __tablename__ = 'country'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.VARCHAR)
    author = db.relationship('Author', backref='country', cascade='all, delete-orphan', lazy='dynamic')


class Author(db.Model):
    """Model for storing authors"""
    __tablename__ = 'author'
    id = db.Column('id', db.Integer, primary_key=True)
    # Foreign key to country from which author belongs
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    name = db.Column('name', db.VARCHAR)
