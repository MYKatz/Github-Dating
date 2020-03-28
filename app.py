#Basic flask app

from flask import Flask, request, url_for, g, session, redirect
from flask import render_template_string, jsonify
from flask_github import GitHub #Github authentication

import numpy as np

from base64 import b64decode

from vars import *
from utils import remove_non_alphanumeric, form_language_feature_vector
from doc2vec import doc2vec

app = Flask(__name__)

#Environment variables
app.config["GITHUB_CLIENT_ID"] = GITHUB_ID
app.config["GITHUB_CLIENT_SECRET"] = GITHUB_SECRET
app.config["SECRET_KEY"] = 'development key'
app.config["DEBUG"] = True

github = GitHub(app)

#Database setup
from sqlalchemy import create_engine, Column, Integer, String, Table, Binary
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(DATABASE_URI) #from vars
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()



#User shcema for db
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    github_access_token = Column(String(255))
    github_id = Column(Integer)
    github_login = Column(String(255))
    name = Column(String(255))
    org = Column(String(255))
    blog = Column(String(255))
    email = Column(String(255))
    embedding = Column(Binary)

    def __init__(self, github_access_token):
        self.github_access_token = github_access_token

class Pair(Base):
    __tablename__ = 'pairs'

    hash = Column(String(32), primary_key=True)
    user_1 = Column(Integer)
    user_2 = Column(Integer)
    u1_liked = Column(Integer)
    u2_liked = Column(Integer)

    def __init__(self, u1, u2):
        self.user_1 = u1
        self.user_2 = u2
        self.u1_liked = 0
        self.u2_liked = 0
        self.hash = hash(f'{min(u1, u2)}-{max(u1, u2)}') #lower one always first


def init_db():
    Base.metadata.create_all(bind=engine)

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

@app.route("/makefeatures")
def makefeatures():
    try:
        user = User.query.filter_by(github_id=g.user.github_id).first()
        if user.embedding:
            return "User already has embedding"
        features = make_feature_vectors()
        user.embedding = features.tobytes() #convert to binary data format
        db_session.commit()
        return "Successfully generated feature vector"
    except:
        return "Feature vector generation failed"

@app.route("/getfeatures")
def getfeatures():
    user = User.query.filter_by(github_id=g.user.github_id).first()
    if user.embedding:
        return str(np.frombuffer(user.embedding))


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

    user.github_access_token = oauth_token

    g.user = user
    github_user = github.get('/user')
    user.github_id = github_user['id']
    user.github_login = github_user['login']
    user.name = github_user["name"]
    user.org = github_user["company"]
    user.blog = github_user["blog"]
    user.email = github_user["email"]

    #check to see if this user already 
    check_user = User.query.filter_by(github_id=user.github_id).first() #github id should also be unique :)
    if not check_user:
        g.user = user
        db_session.add(user)
        session['user_id'] = user.id
    else:
        #we don't actually add the new user object if a previous user with this ID exists
        check_user.github_access_token = oauth_token
        g.user = check_user
        session['user_id'] = check_user.id


    
    #db_session.add(user) this may only be necessary in certain situations
    
    db_session.commit()

    #dumb hack to get user ids to work.
    #TODO: make this better... sometime
    usr = User.query.filter_by(github_id=g.user.github_id).first()
    g.user = usr
    session['user_id'] = usr.id

    return redirect(next_url)

# Github/user data utils

def get_repos():
    """ Returns a list of repo urls and a list of main languages for those repos """

    github_user = github.get('/user')
    repos = github.get(github_user["repos_url"])
    return [repo["url"] for repo in repos], [repo["language"] for repo in repos]


def make_doc_from_repos(repos):
    """ Makes one cohesive document from the readmes of a list of links to repos """

    out = ''

    for repo_url in repos:
        try:
            readme = github.get(f'{repo_url}/readme')
        except:
            continue
        if readme["content"]:
            content_no_newlines = readme["content"].replace("\n", "")
            content_markdown = str(b64decode(content_no_newlines))
            content_text = remove_non_alphanumeric(content_markdown)
            out += content_text #could make this more efficient by collecting it in a list, then joining

    return out

def make_feature_vectors():
    repos, langs = get_repos()
    big_doc = make_doc_from_repos(repos) #concatenated readmes

    lang_features = form_language_feature_vector(langs)
    readme_features = doc2vec(big_doc)

    return np.concatenate((readme_features, lang_features))



if __name__ == "__main__":
    init_db()
    print("Initialized database")