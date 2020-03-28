#Basic flask app

from flask import Flask, request, url_for, g, session, redirect
from flask import render_template_string, jsonify
from flask_github import GitHub #Github authentication

from vars import *

app = Flask(__name__)

#Environment variables
app.config["GITHUB_CLIENT_ID"] = GITHUB_ID
app.config["GITHUB_CLIENT_SECRET"] = GITHUB_SECRET
app.config["SECRET_KEY"] = 'development key'
app.config["DEBUG"] = True

github = GitHub(app)

#Database setup
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(DATABASE_URI) #from vars
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)


#User shcema for db
#TODO: actually make this. Should include some way to store feature vector
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    github_access_token = Column(String(255))
    github_id = Column(Integer)
    github_login = Column(String(255))

    def __init__(self, github_access_token):
        self.github_access_token = github_access_token




@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@app.after_request
def after_request(response):
    db_session.remove()
    return response

@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user.github_access_token



#Actual routes begin here
@app.route("/index")
@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/profile')
def getProfile():
    return f"You are github user #{str(g.user.github_id)}"

@app.route('/login')
def login():
    return github.authorize()

@app.route('/login-callback')
@github.authorized_handler
def authorized(oauth_token):
    next_url = request.args.get('next') or url_for('index')
    if oauth_token is None:
        flash("Authorization failed.")
        return redirect(next_url)

    user = User.query.filter_by(github_access_token=oauth_token).first()
    if user is None:
        user = User(oauth_token)
        db_session.add(user)

    user.github_access_token = oauth_token

    g.user = user
    github_user = github.get('/user')
    user.github_id = github_user['id']
    user.github_login = github_user['login']

    db_session.commit()

    session['user_id'] = user.id

    return redirect(next_url)

if __name__ == "__main__":
    init_db()
    print("Initialized database")