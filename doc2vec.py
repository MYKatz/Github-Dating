from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import get_tmpfile

import os

import numpy as np

model_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "model"))
model_path = os.path.join(model_dir, "doc2vec.model")
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

def doc2vec(inp):
    """ Returns the embedding of the input document """
    model = Doc2Vec.load(model_path)
    vec = model.infer_vector(inp.split(" "))
    return (vec - np.min(vec))/np.ptp(vec) #normalize the vector to [0, 1]

def train_if_not_exist():
    """ Trains doc2vec model (if one already doesn't exist) and saves it to disk """
    if not os.path.exists(model_path):
        documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(common_texts)]
        model = Doc2Vec(documents, vector_size=64, window=2, min_count=1, workers=4, epochs=10000)
        model.save(model_path)

if __name__ == "__main__":
    train_if_not_exist()    
