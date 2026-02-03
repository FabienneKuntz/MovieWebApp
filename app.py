from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
from models import db, Movie, User
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data/movies.db')
# Create 'data' folder if it doesn't exist
os.makedirs(os.path.dirname(db_path), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models

data_manager = DataManager() # Create an object of your DataManager class


@app.route('/', methods=['GET'])
def index():
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    name = request.form['name']
    data_manager.create_user(name)
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_movies(user_id):
    movies = data_manager.get_movies(user_id)
    user = next((u for u in data_manager.get_users() if u.id == user_id), None)

    if not user:
        return "User not found", 404

    return render_template('movies.html', user=user, movies=movies)


# @app.route('/users/<int:user_id>/movies', methods=['POST'])
# pass
#
#
# @app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
# pass
#
#
# @app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
# pass


if __name__ == '__main__':
  with app.app_context():
    db.create_all()

    app.run()
