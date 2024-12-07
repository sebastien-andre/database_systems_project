import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",    
    password="" 
)
cursor = conn.cursor()

# Create the database if it doesn't exist
cursor.execute('CREATE DATABASE IF NOT EXISTS forum')
cursor.execute('USE forum')

# Create the Overboard table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Overboard (
    overboard_id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT,
    name VARCHAR(255)
)
''')

# Create the Topic table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Topic (
    topic_id INT AUTO_INCREMENT PRIMARY KEY,
    overboard_id INT,
    creation_date DATETIME,
    created_by VARCHAR(255),
    title VARCHAR(255),
    FOREIGN KEY (overboard_id) REFERENCES Overboard(overboard_id)
        ON DELETE CASCADE ON UPDATE CASCADE
)
''')

# Create the User table
cursor.execute('''
CREATE TABLE IF NOT EXISTS User (
    user_name VARCHAR(255) PRIMARY KEY,
    registration_date DATETIME,
    email VARCHAR(255),
    password VARCHAR(255)
)
''')

# Create the UserProfile table
cursor.execute('''
CREATE TABLE IF NOT EXISTS UserProfile (
    user_name VARCHAR(255),
    profile_id INT AUTO_INCREMENT PRIMARY KEY,
    avatar VARCHAR(255),
    location VARCHAR(255),
    FOREIGN KEY (user_name) REFERENCES User(user_name)
        ON DELETE CASCADE ON UPDATE CASCADE
)
''')

# Create the Image table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Image (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255)
)
''')


# Create the ImageSubjects table
cursor.execute('''
CREATE TABLE IF NOT EXISTS ImageSubjects (
    image_id INT,
    subject VARCHAR(255),
    FOREIGN KEY (image_id) REFERENCES Image(image_id)
        ON DELETE CASCADE ON UPDATE CASCADE
)
''')

# Create the PostTags table
cursor.execute('''
CREATE TABLE IF NOT EXISTS PostTags (
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
)
''')

# Create the Post table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Post (
    user_name VARCHAR(255),
    profile_id INT,
    overboard_id INT,
    topic_id INT,
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    image_id INT,
    tag_id INT,
    post_date DATETIME,
    content TEXT,
    reply_to_post_id INT,
    FOREIGN KEY (user_name) REFERENCES User(user_name)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (profile_id) REFERENCES UserProfile(profile_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (overboard_id) REFERENCES Overboard(overboard_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES Topic(topic_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (image_id) REFERENCES Image(image_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES PostTags(tag_id)
        ON DELETE SET NULL ON UPDATE CASCADE
)
''')

conn.commit()
conn.close()

print("Database \"forum\" setup complete!")





