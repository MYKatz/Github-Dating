#Nearest-neighbor implementation

from sqlalchemy import create_engine, Column, Integer, String, Table, Binary
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import numpy as np
import os
from annoy import AnnoyIndex

from vars import DATABASE_URI
from schemas import User

engine = create_engine(DATABASE_URI) #from vars
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

model_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "model"))
model_path = os.path.join(model_dir, "index.hnsw")
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

#load model
u = User.query.one()
#we assume that dimensionality will be the same for all users
dim = np.frombuffer(u.embedding).size #dimensionality
index = AnnoyIndex(dim, 'euclidean')
index.load(model_path)


def create_new_index():
    """ Loops through the database and indexes all users into an approximate knn model """

    query = User.query.all()

    if len(query) == 0:
        return
    
    #we assume that dimensionality will be the same for all users
    u = query[0]
    dim = np.frombuffer(u.embedding).size #dimensionality
    index = AnnoyIndex(dim, 'euclidean') #euclidean distance for now. TODO: look into other metrics

    for user in query:
        if user.embedding:
            ind = user.id
            embedding = np.frombuffer(user.embedding)
            index.add_item(ind, embedding)

    index.build(10) #build the index with 10 trees. After this, it can't be edited
    index.save(model_path)
    return ind + 1

def get_neighbors(id, k):
    if id < index.get_n_items(): #the vector has been indexed!
        return index.get_nns_by_item(id, k) #k nearest neighbors
    else: #this user has not been indexed yet, we need to use their actual vector
        usr = User.query.get(id=id).first()
        if usr.embedding:
            v = np.frombuffer(usr.embedding) 
            return index.get_nns_by_vector(v, k)
        else:
            return [] #hopefully we handle this on the front-end, only allowing users with their embeddings to see potential matches

def make_pairs(id):
    k = max(50, min(index.get_n_items() / 5, 200)) #eh idk if this is necessary lol
    last_k = 0
    found = 0
    i = 0
    while found < 15 and i < 5 and k < index.get_n_items(): #loop until we get a satisfactory amount (15 for now), or for 5 iterations
        i += 1
        neighbors = get_neighbors(id, k)[last_k:]
        for neighbor in neighbors:
            p = Pair.query.filter_by(hash=f'{min(id, neighbor)}-{max(id, neighbor)}').first()
            if not p:
                found += 1
                new_pair = Pair(min(id, neighbor), max(id, neighbor))
                db_session.add(new_pair)

    db_session.commit()


        
    

if __name__ == "__main__":
    print("Creating index...")
    n = create_new_index()
    print(f"Finished creating index. N items = {n}") #all users with ids below this number are accounted for, and all those not are not