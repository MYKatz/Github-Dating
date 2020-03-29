#Database setup
from sqlalchemy import create_engine, Column, Integer, String, Table, Binary
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from vars import *

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
    discord = Column(String(255))
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
        self.hash = str(hash(f'{min(u1, u2)}-{max(u1, u2)}')) #lower one always first
