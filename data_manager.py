from models import db, User, Movie
import requests
import os
from dotenv import load_dotenv

load_dotenv()
MOVIES_API_KEY = os.getenv("MOVIES_API_KEY")


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
            print("Movie not found.")
            return None

        movie = Movie(
            title=data.get("Title"),
            year=int(data.get("Year")) if data.get("Year") else None,
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

