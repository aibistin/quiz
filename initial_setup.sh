rm -rf migrations
flaskenv_file=".flaskenv"
dev_db_name="quiz_dev_db.db"
rm -f "${dev_db_name}"
mkdir logs > /dev/null 2>&1

echo '# Note: This would normally be added to the .gitignore'  >| "${flaskenv_file}"
echo                                                           >> "${flaskenv_file}"
echo 'FLASK_APP="quiz.py"'                                     >> "${flaskenv_file}"
echo 'DEV_DATABASE_URL="sqlite:///../${dev_db_name}"'          >> "${flaskenv_file}"
echo 'TEST_DATABASE_URL="sqlite:///../quiz_test_db.db"'        >> "${flaskenv_file}"
echo 'FLASK_APP="quiz.py"'                                     >> "${flaskenv_file}"
echo 'FLASK_DEBUG="1"'                                         >> "${flaskenv_file}"
echo                                                           >> "${flaskenv_file}"

export DEV_DATABASE_URL="${DEV_DATABASE_URL}"

rm -f "${DEV_DATABASE_URL}"
flask db init
flask db migrate -m "New DB"
flask db upgrade
sqlite3 "${dev_db_name}" < ./data/init_db_sql.sql
flask run
