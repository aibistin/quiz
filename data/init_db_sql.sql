-- Run the below command to seed the database.
-- sqlite3 app.db < ./data/init_db_sql.sql
--
-- INSERT INTO user ('first_name',  'last_name', 'email',  'last_seen',  created) VALUES ('Jake',  'Flake', 'jake@flake.com',  '2020-08-18 00:31:05.500490',  '2020-08-18 00:31:05.500490');
-- INSERT INTO user ('first_name',  'last_name', 'email',  'last_seen',  created ) VALUES ('Fred',  'Flint', 'fred@flint.com',  '2020-08-18 00:31:05.500490',  '2020-08-18 00:31:05.500490');


INSERT into question (body, answer) VALUES ('Whats the capital of Italy',  'Rome');
INSERT into question (body, answer) VALUES ('Whats the capital of Spain',  'Madrid');
INSERT into question (body, answer) VALUES ('Whats the capital of England',  'London');
INSERT into question (body, answer) VALUES ('Whats the correct answer from this file',  '42');


INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Napels',1,0 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Turin',1,0 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Rome',1,1 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Paris',1,0 );

INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Barcelona',2,0 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Seville',2,0 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Madrid',2,1 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Paris',2,0 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('New York',2,0 );

INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Dublin',3,0 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('London',3,1 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Glasgow',3,0 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Paris',3, 0 );
INSERT INTO option ( body,  question_id, is_answer ) VALUES ('Milton Keynes',3,0 );


INSERT into user_questions (user_id, question_id, is_correct) VALUES (1, 1, 0);
INSERT into user_questions (user_id, question_id, is_correct) VALUES (1, 2, 1);
INSERT into user_questions (user_id, question_id, is_correct) VALUES (1, 3, 0);

INSERT into user_questions (user_id, question_id, is_correct) VALUES (2, 1, 1);
INSERT into user_questions (user_id, question_id, is_correct) VALUES (2, 2, 0);
INSERT into user_questions (user_id, question_id, is_correct) VALUES (2, 3, 1);



INSERT INTO File ( location,  question_id ) VALUES ('./data/question_one_file.txt',  1 );


