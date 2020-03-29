# Github Dating

Made for Winhacks 2020, by Matthew Katz and Galaxia Wu


## Getting up and running

Run app.py once in python to initialize the DB. You'll need to comment out the "import nearest" (currently line 17). Why? Because Matthew Katz is a clown.

Run doc2vec.py once to initialize our doc2vec model

Run nearest.py (as main, just like the others) every so often (ie 15 mins, 30 mins) to update knn model in batches. Use a cron job or something.

Then use flask run to run the flask server and pray to god it works.


## SQL schemas

### Users

```sql
CREATE TABLE users (
    id Integer PRIMARY KEY
    github_access_token VARCHAR(255)
    github_id = Integer
    github_login VARCHAR(255)
)
```

### Pairs (potential matches)

```sql
CREATE TABLE pairs (
    hash VARCHAR(32) PRIMARY KEY, --hash of ("{min(id1, id2)}-{max(id1, id2)}"), should be unique
    user_1 Integer, --user ids
    user_2 Integer,
    u1_liked Integer -- 0 for not seen yet, -1 for dislike, 1 for like
    u2_liked Integer -- same as above
)
```

There will undoubtedly be collisions but oh well :shrug: