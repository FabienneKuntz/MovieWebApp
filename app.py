from flask import Flask
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


@app.route('/', METHODS=['GET'])
def home():
    return "Welcome to MoviWeb App!"


@app.route('/users', methods=['POST'])
def list_users():
    users = data_manager.get_users()
    return str(users)


@app.route('/users/<int:user_id>/movies', methods=['GET'])
pass


@app.route('/users/<int:user_id>/movies', methods=['POST'])
pass


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
pass


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
pass


if __name__ == '__main__':
  with app.app_context():
    db.create_all()

    app.run()
