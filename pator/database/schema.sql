DROP TABLE IF EXISTS tutee_course_favorite;
DROP TABLE IF EXISTS tutor_session_review;
DROP TABLE IF EXISTS tutor_session;
DROP TABLE IF EXISTS course_tutor_keyword;
DROP TABLE IF EXISTS course_tutor;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS tutee;
DROP TABLE IF EXISTS tutor;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    NIM CHAR(10) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    prodi VARCHAR(100) NOT NULL,
    angkatan INT
);

CREATE TABLE tutee (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    average_rating_given TINYINT, 
    user_id BIGINT UNIQUE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
);

CREATE TABLE tutor (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    number_of_unique_tutee INT,
    self_description LONGTEXT,
    average_rating TINYINT,
    user_id BIGINT UNIQUE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
);

CREATE TABLE course (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(255) NOT NULL,
    course_prodi VARCHAR(255) NOT NULL
);

CREATE TABLE course_tutor (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    tutor_id BIGINT NOT NULL,
    course_id BIGINT NOT NULL,
    hourly_fee DECIMAL(10) NOT NULL,
    course_description LONGTEXT,
    course_rating TINYINT, 
    FOREIGN KEY (tutor_id) REFERENCES tutor (id),
    FOREIGN KEY (course_id) REFERENCES course (id)
);

CREATE TABLE course_tutor_keyword (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    keyword VARCHAR(255) NOT NULL,
    course_tutor_id BIGINT NOT NULL,
    FOREIGN KEY (course_tutor_id) REFERENCES course_tutor (id)
);

CREATE TABLE tutor_session (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    tutor_id BIGINT NOT NULL,
    tutee_id BIGINT NOT NULL,
    course_tutor_id BIGINT NOT NULL,
    date_started DATE,
    date_ended DATE,
    FOREIGN KEY (tutor_id) REFERENCES tutor (id),
    FOREIGN KEY (tutee_id) REFERENCES tutee (id),
    FOREIGN KEY (course_tutor_id) REFERENCES course_tutor (id)
);

CREATE TABLE tutor_session_review (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    tutee_rating TINYINT,
    tutee_review LONGTEXT,
    tutor_session_id BIGINT UNIQUE NOT NULL,
    FOREIGN KEY (tutor_session_id) REFERENCES tutor_session (id)
);

CREATE TABLE tutee_course_favorite (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    tutee_id BIGINT NOT NULL,
    course_tutor_id BIGINT NOT NULL,
    date_added DATE,
    FOREIGN KEY (tutee_id) REFERENCES tutee (id),
    FOREIGN KEY (course_tutor_id) REFERENCES course_tutor (id)
);