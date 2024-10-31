-- setup.sql
CREATE DATABASE IF NOT EXISTS forum;

USE forum;

CREATE TABLE IF NOT EXISTS Overboard (
    overboard_id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Topic (
    topic_id INT AUTO_INCREMENT PRIMARY KEY,
    overboard_id INT,
    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(255),
    title VARCHAR(255),
    FOREIGN KEY (overboard_id) REFERENCES Overboard(overboard_id)
);

CREATE TABLE IF NOT EXISTS User (
    user_name VARCHAR(255) PRIMARY KEY,
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    email VARCHAR(255),
    password VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS UserProfile (
    user_name VARCHAR(255),
    profile_id INT AUTO_INCREMENT PRIMARY KEY,
    avatar VARCHAR(255),
    location VARCHAR(255),
    FOREIGN KEY (user_name) REFERENCES User(user_name)
);

CREATE TABLE IF NOT EXISTS Image (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    content BLOB
);

CREATE TABLE IF NOT EXISTS ImageSubjects (
    image_id INT,
    subject VARCHAR(255),
    FOREIGN KEY (image_id) REFERENCES Image(image_id)
);

CREATE TABLE IF NOT EXISTS PostTags (
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Post (
    user_name VARCHAR(255),
    profile_id INT,
    overboard_id INT,
    topic_id INT,
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    image_id INT,
    tag_id INT,
    post_Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    content TEXT,
    reply_to_post_id INT,
    FOREIGN KEY (user_name) REFERENCES User(user_name),
    FOREIGN KEY (profile_id) REFERENCES UserProfile(profile_id),
    FOREIGN KEY (overboard_id) REFERENCES Overboard(overboard_id),
    FOREIGN KEY (topic_id) REFERENCES Topic(topic_id),
    FOREIGN KEY (image_id) REFERENCES Image(image_id),
    FOREIGN KEY (tag_id) REFERENCES PostTags(tag_id)
);


