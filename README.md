# Quiz

## Quiz backend API with Flask

### Tested with Python 3.8.3

### Install and Setup the Python Environment

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

#### To Setup the database and Run the Application

```bash

./initial_setup.sh

flask run 

# Sample output
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
[2021-08-15 14:16:15,105] INFO in __init__: Quiz startup
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

The Application URI: http://127.0.0.1:5000/

##### To run a very basic database test suite

```bash
flask test
```

### Sample usage with Postman

#### Start by sending a POST request with user data

```json
{
  "first_name" : "joe",
  "last_name"  : "soap",
  "email"      : "joe@soap.com"
}
```

##### This will retrun something like

```json
{
  "delta_time_seconds": 4597,
  "email": "joe@soap.com",
  "first_name": "joe",
  "id": 1,
  "last_name": "soap",
  "test_url": "http://127.0.0.1:5000/test/%252FHMZqDT35VLOVbPhKzG1OwHqlHYkyknl",
  "remaining_time_seconds": 3599,
  "token_expire_time": "2021-09-15T03:14:50.171165Z",
  "username": "Joe Soap"
}
```

##### Use the "test_url" to return the first and subsequent questions data using GET

```GET: http://127.0.0.1:5000/test/%252FHMZqDT35VLOVbPhKzG1OwHqlHYkyknl```

__Note__: Keep the "user_token" for future requests.

###### Returned JSON

```json
{
  "current_question": {
    "answer": "Rome",
    "body": "Whats the capital of Italy",
    "files": [
      {
        "id": 1,
        "location": "./data/question_one_file.txt",
        "question_id": 1
      }
    ],
    "id": 1,
    "options": [
      {
        "body": "Napels",
        "id": 1,
        "is_answer": false,
        "question_id": 1
      },
      ...
         ]
  },
  "test_url": "http://127.0.0.1:5000/test/%252FHMZqDT35VLOVbPhKzG1OwHqlHYkyknl",
  "user": {
    "delta_time_seconds": 4735,
    "email": "joe@soap.com",
    "first_name": "joe",
    "id": 1,
    "last_name": "soap",
    "remaining_time_seconds": 3462,
    "token_expire_time": "2021-09-15T03:14:50.171165Z",
    "username": "Joe Soap"
  },
}
```

##### To Answer the First Question send a POST request with the sample JSON below

```http://127.0.0.1:5000/test/02yWrSI6BbYb9emRo56%2BUotTR7%2BQd4UB```

```json
{
    "AnsweredText": null,
    "ChildQuestionAnsweredText": null,
    "ChildQuestionAnsweredText2": null,
    "OptionId": 4,
    "QuestionId": "1"
}
```

###### This will return the second question JSON

Repeat until no more questions.

Run ```./initial_setup.sh``` to start over.

### TODO

1. Input validation.
2. Don't include the correct answer info. with the question JSON.
3. When all questions have been answered, redirect to the survey and tally the correct answers.
4. More tests.
5. Create a production config setup.
6. The possibilites are endless, but thats enough for now.
