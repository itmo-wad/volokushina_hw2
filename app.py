from flask import Flask, render_template, redirect, url_for, request
from peewee import *
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(__name__)

DATABASE = 'postgresql://postgres:1234@localhost:5432/hw2'
db = PostgresqlDatabase('hw2', user='postgres', password='1234', host='localhost', port=5432)

login_manager = LoginManager()
login_manager.init_app(app)


class User(Model):
    username = TextField(unique=True)
    password = TextField()

    @classmethod
    def create_user(cls, username, password):
        user = cls.create(
            username=username,
            password=password
        )
        return user

    class Meta:
        database = db
        db_table = 'user'
        scheme = 'public'

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
            if user and user.password == password:
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
    db.connect()
    db.create_tables([User], safe=True)
    db.close()
    app.run(debug=True, host='localhost', port=5000)
