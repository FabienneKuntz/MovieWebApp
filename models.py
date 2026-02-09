from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User id={self.id} name='{self.name}'>"


class Movie(db.Model):
    # Define all the Movie properties
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer)
    rating = db.Column(db.Float, nullable=True)
    director = db.Column(db.String)
    poster_url = db.Column(db.String)
    imdb_id  = db.Column(db.String)
    # Link Movie to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)