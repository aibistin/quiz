# Quiz
## Quiz backend API with flask
##### Tested with Python 3.8.3

### Setup

```bash 
git clone quiz
cd quiz
apt-get install python3-venv
pip install flask
pip install --upgrade pip
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```



# Creat a flaskenv file .flaskenv
## Add .flaskenv to the .gitignore


```bash 
flask run 
 Serving Flask app "quiz.py"
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
[2021-08-15 14:16:15,105] INFO in __init__: Quiz startup
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

#-------------------------------------------
$ flask shell > > > from hello import db > > > db.create_all()

## pip install flask-migrate
## flask db init
### After creating the db
## flask db migrate
### After changes
##### flask db upgrade
#### sqlite3 app.db < ./data/init_db_sql.sql