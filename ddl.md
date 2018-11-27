```
CREATE TABLE users (
	   user_id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	   username VARCHAR(40) NOT NULL UNIQUE,
	   password CHAR(60) NOT NULL,
	   bio TEXT,
	   join_date TIMESTAMP NOT NULL
);


CREATE TABLE posts (
	   post_id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	   title VARCHAR(255) NOT NULL,
	   content TEXT NOT NULL,
	   created TIMESTAMP,
	   user_id INT(10) UNSIGNED NOT NULL,
	   post_id VARCHAR(80),
	   FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE comments (
	   comment_id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	   content TEXT NOT NULL,
	   user_id INT(10) UNSIGNED NOT NULL,
	   post_id INT(10) UNSIGNED NOT NULL,
	   FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
	   FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE
);

CREATE TABLE topics (
	   topic_id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	   topic VARCHAR(100) NOT NULL,
	   description TEXT
);


CREATE TABLE quizzes (
	   quiz_id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	   title VARCHAR(255) NOT NULL,
	   description TEXT
);

CREATE TABLE questions (
	   question_id INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	   question TEXT NOT NULL,
	   solution TEXT NOT NULL,
	   question_type INT(10) NOT NULL
);

CREATE TABLE followers (
	   follower_id INT(10) UNSIGNED NOT NULL,
	   follows_id INT(10) UNSIGNED NOT NULL,
	   PRIMARY KEY (follower_id, follows_id),
	   FOREIGN KEY (follower_id) REFERENCES users(user_id) ON DELETE CASCADE,
	   FOREIGN KEY (follows_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE user_topic (
	   user_id INT(10) UNSIGNED NOT NULL,
	   topic_id INT(10) UNSIGNED NOT NULL,
	   PRIMARY KEY (user_id, topic_id),
	   FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
	   FOREIGN KEY (topic_id) REFERENCES topics(topic_id) ON DELETE CASCADE
);

CREATE TABLE post_quiz (
	   post_id INT(10) UNSIGNED NOT NULL,
	   quiz_id INT(10) UNSIGNED NOT NULL,
	   PRIMARY KEY (post_id, quiz_id),
	   FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE,
	   FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id) ON DELETE CASCADE
);

CREATE TABLE post_topic (
	  post_id INT(10) UNSIGNED NOT NULL,
	  topic_id INT(10) UNSIGNED NOT NULL,
	  PRIMARY KEY (post_id, topic_id),
	  FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE,
	  FOREIGN KEY (topic_id) REFERENCES topics(topic_id) ON DELETE CASCADE
);

CREATE TABLE user_likes_post (
	   user_id INT(10) UNSIGNED NOT NULL,
	   post_id INT(10) UNSIGNED NOT NULL,
	   PRIMARY KEY (user_id, post_id),
	   FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
	   FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE
);
```