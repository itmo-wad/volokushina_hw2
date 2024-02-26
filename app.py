from flask import Flask, render_template, redirect, url_for, request
from peewee import Model, TextField, PostgresqlDatabase
import psycopg2
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = str(secrets.token_hex())

DATABASE = 'hw2'
USER = 'postgres'
PASSWORD = 1234
HOST = 'localhost'
PORT = 5432

db = PostgresqlDatabase(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)

login_manager = LoginManager()
login_manager.init_app(app)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel, UserMixin):
    username = TextField(unique=True)
    password = TextField()

    @classmethod
    def create_user(cls, username, password, safe=True):
        if safe:
            check_user = cls.select().where(cls.username == username).exists()
            if check_user:
                return "user exists"
        user = cls.create(
            username=username,
            password=generate_password_hash(password)
        )
        return user

    class Meta:
        db_table = 'user'

db.connect()
db.create_tables([User], safe=True)

User.create_user("ksylik", "1234", safe=True)
db.close()

@login_manager.user_loader
def load_user(user_id):
    return User.get(User.id == int(user_id))

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = User.get(User.username == username)
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('profile'))
            else:
                return 'Invalid username or password'
        except User.DoesNotExist:
            return 'User does not exist'
    return render_template('login.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
