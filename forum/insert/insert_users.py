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
    ("goofy", "goofy@disney.com", "Goofy", "Goofy's Avatar URL", "Toontown"),
    ("pluto", "pluto@disney.com", "Pluto", "Pluto's Avatar URL", "Toontown"),
    ("snow.white", "snowwhite@disney.com", "Snow White", "Snow White's Avatar URL", "The Woods"),
    ("cinderella", "cinderella@disney.com", "Cinderella", "Cinderella's Avatar URL", "Kingdom of Arendelle"),
    ("ariel", "ariel@disney.com", "Ariel", "Ariel's Avatar URL", "The Ocean"),
    ("simba", "simba@disney.com", "Simba", "Simba's Avatar URL", "Pride Lands"),
    ("belle", "belle@disney.com", "Belle", "Belle's Avatar URL", "Village"),
    ("woody", "woody@disney.com", "Woody", "Woody's Avatar URL", "Toy Story Land"),
    ("buzz.lightyear", "buzz@disney.com", "Buzz Lightyear", "Buzz's Avatar URL", "Toy Story Land"),
    ("tigger", "tigger@disney.com", "Tigger", "Tigger's Avatar URL", "Hundred Acre Wood"),
    ("pooh", "pooh@disney.com", "Winnie the Pooh", "Pooh's Avatar URL", "Hundred Acre Wood"),
    ("stitch", "stitch@disney.com", "Stitch", "Stitch's Avatar URL", "Hawaii"),
    ("elsa", "elsa@disney.com", "Elsa", "Elsa's Avatar URL", "Kingdom of Arendelle"),
    ("anna", "anna@disney.com", "Anna", "Anna's Avatar URL", "Kingdom of Arendelle"),
    ("maleficent", "maleficent@disney.com", "Maleficent", "Maleficent's Avatar URL", "Dark Woods"),
    ("jack.sparrow", "jack@disney.com", "Jack Sparrow", "Jack's Avatar URL", "Caribbean"),
    ("hades", "hades@disney.com", "Hades", "Hades' Avatar URL", "Underworld")
]

def insert_users():
    """Insert Disney users into the forum database."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor()

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

            connection.commit()
            print("Successfully inserted users.")

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    insert_users()
