# Github Dating

Made for Winhacks 2020, by Matthew Katz and Galaxia Wu


## Getting up and running

Run app.py once in python to initialize the DB

Then use flask run to run the flask server


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