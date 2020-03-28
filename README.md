# Github Dating

Made for Winhacks 2020, by Matthew Katz and Galaxia Wu


## Getting up and running

Run app.py once in python to initialize the DB

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