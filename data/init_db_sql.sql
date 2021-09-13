-- Run the below command to seed the database.
-- sqlite3 app.db < ./data/init_db_sql.sql
--
DELETE FROM user;
DELETE FROM option;
DELETE FROM file;
DELETE FROM question;
DELETE FROM user_question;


INSERT into question (body, answer) VALUES ('Whats the capital of Italy', 'Rome');
INSERT into question (body, answer) VALUES ('Whats the capital of Spain', 'Madrid');
INSERT into question (body, answer) VALUES ('Whats the capital of England', 'London');
INSERT into question (body, answer) VALUES ('Whats the correct answer from this file', '42');
INSERT into question (body, answer) VALUES ('What is 2 + 2', '22');
INSERT into question (body, answer) VALUES ('How many boroughs in New York City', '5');


INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Napels', 1, 0 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Turin', 1, 0 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Rome', 1, 1 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Paris', 1, 0 );


INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Barcelona', 2, 0 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Seville', 2, 0 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Madrid', 2, 1 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Paris', 2, 0 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('New York', 2, 0 );


INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Dublin', 3, 0 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('London', 3, 1 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Glasgow', 3, 0 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Paris', 3, 0 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Milton Keynes', 3, 0 );


INSERT INTO File ( location,  question_id ) VALUES ('./data/question_one_file.txt',  1 );

INSERT INTO option ( body,  question_id, is_answer ) VALUES ('4', 5, 0 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('5', 5, 0 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('6', 5, 0 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('22', 5, 1 );


INSERT INTO option ( body,  question_id, is_answer ) VALUES ('1', 6, 0 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('2', 6, 0 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('6', 6, 0 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('5', 5, 1 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('10', 5, 0 );

