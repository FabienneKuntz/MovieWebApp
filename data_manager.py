from models import db, User, Movie
import requests
import os
from dotenv import load_dotenv

load_dotenv()
MOVIES_API_KEY = os.getenv("MOVIES_API_KEY")


class MovieNotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)

class DataManager():
  # Define Crud operations as methods
    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()


    def get_users(self):
        return User.query.all()


    def get_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()


    def add_movie(self, user_id, movie):
        # Get movie info from OMDb
        api_url = f"http://www.omdbapi.com/?t={movie}&apikey={MOVIES_API_KEY}"
        response = requests.get(api_url)
        if response.status_code != 200:
            print("Error retrieving movie information")
            return None

        data = response.json()
        if data.get("Response") != "True":
            raise MovieNotFoundError(f"Movie '{movie}' not found.")

        rating_str = data.get("imdbRating")
        try:
            rating = float(rating_str) if rating_str and rating_str != "N/A" else None
        except ValueError:
            rating = None

        imdb_id = data.get("imdbID")
        poster_url = f"https://img.omdbapi.com/?apikey={MOVIES_API_KEY}&i={imdb_id}" if imdb_id else None


        movie = Movie(
            title=data.get("Title"),
            year=int(data.get("Year")) if data.get("Year") else None,
            director=data.get("Director"),
            rating=rating,
            imdb_id = data.get("imdbID"),
            poster_url = poster_url,
            user_id=user_id
            )

        db.session.add(movie)
        db.session.commit()

        return movie


    def update_movie(self, movie_id, new_title):
        movie = Movie.query.get(movie_id)
        if movie:
            movie.title = new_title
            db.session.commit()


    def delete_movie(self, movie_id):
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
