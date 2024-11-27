import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': 'localhost',  # Adjust as necessary
    'user': 'root',
    'password': '3kAF9saj!!!',
    'database': 'forum'
}

# Sample Disney users
DISNEY_USERS = [
    ("mickey.mouse", "mickey@disney.com", "Mickey Mouse", "Mickey's Avatar URL", "Toontown"),
    ("minnie.mouse", "minnie@disney.com", "Minnie Mouse", "Minnie's Avatar URL", "Toontown"),
    ("donald.duck", "donald@disney.com", "Donald Duck", "Donald's Avatar URL", "Duckburg"),
    # Add additional users as needed
]

# Sample Overboards
OVERBOARDS = [
    ("General Discussion", "Talk about anything here!"),
    ("Announcements", "Forum news and updates."),
    ("Support", "Get help and support from the community."),
    ("Off-Topic", "Discuss anything non-forum related."),
    ("Introductions", "Introduce yourself to the community.")
]

# Sample Topics for each overboard
TOPICS = [
    (1, 'mickey.mouse', 'Welcome to General Discussion'),
    (2, 'minnie.mouse', 'Forum Update: New Features'),
    (3, 'donald.duck', 'Need Help with Login Issues'),
    (4, 'goofy', 'Favorite Movies?'),
    (5, 'pluto', 'Hello Everyone!')
]

def insert_data():
    """Truncate tables and insert sample data into the forum database."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor()

            # Truncate tables to clear existing data
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            cursor.execute("TRUNCATE TABLE Topic;")
            cursor.execute("TRUNCATE TABLE Overboard;")
            cursor.execute("TRUNCATE TABLE UserProfile;")
            cursor.execute("TRUNCATE TABLE User;")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

            # Insert users
            for user_name, email, profile_name, avatar, location in DISNEY_USERS:
                password = "Password123!"  # Example password
                registration_date = datetime.now()

                # Insert user
                cursor.execute("""
                    INSERT INTO User (user_name, registration_date, email, password)
                    VALUES (%s, %s, %s, %s)
                """, (user_name, registration_date, email, password))

                # Insert user profile
                cursor.execute("""
                    INSERT INTO UserProfile (user_name, avatar, location)
                    VALUES (%s, %s, %s)
                """, (user_name, avatar, location))

            # Insert Overboards
            for name, description in OVERBOARDS:
                cursor.execute("""
                    INSERT INTO Overboard (name, description)
                    VALUES (%s, %s)
                """, (name, description))

            # Insert Topics
            for overboard_id, created_by, title in TOPICS:
                creation_date = datetime.now()
                cursor.execute("""
                    INSERT INTO Topic (overboard_id, created_by, title, creation_date)
                    VALUES (%s, %s, %s, %s)
                """, (overboard_id, created_by, title, creation_date))

            connection.commit()
            print("Database has been reset and new data inserted successfully.")

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    insert_data()
