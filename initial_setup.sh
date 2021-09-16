rm -rf migrations
flaskenv_file=".flaskenv"
dev_db_name="quiz_dev_db.db"
rm -f "${dev_db_name}"
mkdir logs > /dev/null 2>&1

cat << FLASKENV_STUFF >| ${flaskenv_file}
# Note: This would normally be added to the .gitignore'  >| "${flaskenv_file}"

FLASK_APP="quiz.py"
DEV_DATABASE_URL="sqlite:///../${dev_db_name}"
# TEST_DATABASE_URL="sqlite:///../quiz_test_db.db"
TEST_DATABASE_URL="sqlite://"
FLASK_DEBUG="1"
FLASKENV_STUFF

export DEV_DATABASE_URL="${DEV_DATABASE_URL}"

flask db init
flask db migrate -m "New DB Setup"
flask db upgrade
sqlite3 "${dev_db_name}" < ./data/init_db_sql.sql
