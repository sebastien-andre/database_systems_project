import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
import random

# Database configuration
DB_CONFIG = {
    'host': 'localhost',  
    'user': 'root',
    'password': '',
    'database': 'forum'
}

# Path to the images directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADS_DIR = os.path.join(BASE_DIR, 'forum', 'static', 'uploads')
PFP_DIR = os.path.join(BASE_DIR, 'forum', 'static', 'pfp')



# Images and tags
IMAGES_AND_TAGS = {
    "baby_yoda.jpg": ["star_wars", "cute", "jedi"],
    "beach1.jpg": ["sunset", "waves", "relaxation"],
    "cat_smiling1.jpg": ["happy", "cat", "smiling"],
    "cat_smiling2.jpg": ["content", "cat", "adorable"],
    "chris_pratt_parks_and_rec.jpg": ["comedy", "parks_and_rec", "andy_dwyer"],
    "disaster_girl.jpg": ["meme", "smirk", "fire"],
    "dog_driving1.jpg": ["funny", "dog", "driving"],
    "dog_smiling1.jpg": ["happy", "dog", "playful"],
    "hide_the_pain1.jpg": ["meme", "awkward", "smile"],
    "mountain1.jpg": ["nature", "hiking", "majestic"],
    "pondering.jpg": ["thinking", "philosophical", "reflection"],
    "questioning.png": ["confused", "curious", "doubt"],
    "rocket1.jpg": ["space", "launch", "adventure"],
    "shrek1.jpg": ["ogre", "dreamworks", "movie"],
    "troll_face.jpg": ["meme", "troll", "classic"],
    "carrera_red.jpg": ["car", "carrera", "porsche"],
    "surprised_pikachu.jpg": ["pikachu", "surprised", "reaction"],
    "spongebob_yay.jpg": ["spongebob", "reaction", "yay"],
    "lucid_trip.jpg": ["lucid", "car", "electric"],
    "lucid_vs_tesla.jpg": ["electric", "tesla", "lucid", "car"]
    
}




C_POSTS = [
    {
        "title": "Pointers: Love Them or Hate Them?",
        "content": "Pointers are so powerful, but debugging them can be a nightmare. Any tips?   ![Image](/static/user_uploads/c_pointers.jpg)",
        "replies": [
            {"user_name": "mickey.mouse", "content": "Pointers are tricky! Use tools like Valgrind to catch memory leaks early."},
            {"user_name": "donald.duck", "content": "Mastering pointers is key to understanding C. Start small and practice with examples!"},
        ],
    },
    {
        "title": "C vs C++: Which Should I Learn?",
        "content": "I'm new to programming and wondering if I should start with C or C++. Any advice?   ![Image](/static/user_uploads/c_vs_cpp.jpg)",
        "replies": [
            {"user_name": "minnie.mouse", "content": "C is great for learning low-level concepts, but C++ gives you object-oriented features."},
            {"user_name": "elsa", "content": "Start with C if you want to understand the basics. Move to C++ later for more advanced applications."},
        ],
    },
]



PYTHON_POSTS = [
    {
        "title": "Python vs JavaScript for Beginners",
        "content": "I’m new to programming and torn between learning Python or JavaScript. Any thoughts?   ![Image](/static/user_uploads/python_vs_js.jpg)",
        "replies": [
            {"user_name": "mickey.mouse", "content": "Python is great for beginners because of its simple syntax and versatility."},
            {"user_name": "donald.duck", "content": "JavaScript is essential if you want to do web development, but Python is better for everything else."},
        ],
    },
    {
        "title": "Best Python Libraries for Data Science",
        "content": "I’m diving into data science and need recommendations for Python libraries. What should I start with?   ![Image](/static/user_uploads/python_libraries.jpg)",
        "replies": [
            {"user_name": "elsa", "content": "Pandas and NumPy are must-haves. Learn them well and you’ll go far!"},
            {"user_name": "minnie.mouse", "content": "Add Matplotlib and Seaborn for visualizations. They’re amazing for creating graphs."},
        ],
    },
]



DIABLO_POSTS = [
    {
        "title": "Diablo IV First Impressions",
        "content": "Finally played Diablo IV last night. The graphics and gameplay are next-level!   ![Image](/static/user_uploads/diablo_iv.jpg)",
        "replies": [
            {"user_name": "donald.duck", "content": "How’s the class balance? I’m torn between Rogue and Sorcerer."},
            {"user_name": "elsa", "content": "The open-world design is fantastic. Did you try any world bosses yet?"},
        ],
    },
    {
        "title": "Best Builds for Hardcore Mode",
        "content": "I want to try Hardcore mode in Diablo IV. Any suggestions for survivable builds?   ![Image](/static/user_uploads/diablo_hardcore.jpg)",
        "replies": [
            {"user_name": "goofy", "content": "Barbarian with a tanky build is your best bet for Hardcore mode."},
            {"user_name": "minnie.mouse", "content": "Necromancer with summons can keep enemies off you and increase survivability."},
        ],
    },
]



SKYRIM_POSTS = [
    {
        "title": "Best Skyrim Mods in 2024",
        "content": "I’m replaying Skyrim and looking for the best mods to enhance the experience. Any recommendations?   ![Image](/static/user_uploads/skyrim_mods.jpg)",
        "replies": [
            {"user_name": "donald.duck", "content": "Install ‘SkyUI’ and ‘Unofficial Patch’ first. They’re essentials for any modded playthrough."},
            {"user_name": "elsa", "content": "Try ‘Legacy of the Dragonborn’ for a whole new questline. It’s amazing!"},
        ],
    },
    {
        "title": "Should I Play Skyrim Again?",
        "content": "It’s been years since I played Skyrim. Is it worth revisiting in 2024?   ![Image](/static/user_uploads/skyrim_revisit.jpg)",
        "replies": [
            {"user_name": "mickey.mouse", "content": "Absolutely! With mods and new editions, it’s like a brand-new game every time."},
            {"user_name": "minnie.mouse", "content": "Skyrim never gets old. The community is still active and releasing amazing content."},
        ],
    },
]





# Overboards
OVERBOARDS = [
    ("Cars", "Discussion about cars."),
    ("Programming", "Programming topics."),
    ("Gaming", "Gaming discussion."),
]

# Topics under each overboard
TOPICS = {
    "Cars": ["Porsche", "Lucid", "Volkswagen", "BMW", "Toyota", "Honda"],
    "Programming": ["C", "Rust", "Python"],
    "Gaming": ["Diablo", "Doom", "Minecraft", "Skyrim"],
}


PORSCHE_POSTS = [
    {
        "title": "my new carerra s!",
        "content": "Just got my hands on a Carrera S. It's an absolute dream!   ![Image](/static/user_uploads/carrera_red.jpg) ",
        "replies": [
            {"user_name": "goofy", "content": "Wow, the Carrera S is a masterpiece! How does it handle in corners? Porsche's engineering is top-notch.  ![Image](/static/uploads/surprised_pikachu.jpg)"},
            {"user_name": "daisy.duck", "content": "That’s incredible! I’ve always loved the Carrera series. Have you taken it out for a spin on some twisty roads yet?"},
            {"user_name": "elsa", "content": "A true dream car! Does it have the sports exhaust option? The sound on those is absolutely thrilling."},
            {"user_name": "anna", "content": "Congratulations! Is it a manual or PDK? Both are amazing, but there’s something special about shifting gears yourself."},
            {"user_name": "simba", "content": "Amazing car! Did you get the PASM suspension? It’s a game changer for comfort and handling."},
            {"user_name": "stitch", "content": "So jealous! Have you tried launching it yet? The Carrera S launch control is supposed to be a rocket."},
            {"user_name": "pluto", "content": "I can’t believe you got one! What wheels and tires are you running? I hear the Carrera S is perfect with Michelin PS4s."},
            {"user_name": "mickey.mouse", "content": "That Guards Red paint is iconic! It must turn heads everywhere you go. How’s the cabin tech?"},
            {"user_name": "daisy.duck", "content": "Is it your daily driver, or is this just for weekends? Either way, I’m sure it’s an absolute blast to drive."},
            {"user_name": "goofy", "content": "What options did you go for? Did you get the Sport Chrono Package? That makes the Carrera S even more dynamic on track days."}
        ],
    },
    {
        "title": "gt3 vs gt3rs on track?",
        "content": "Thinking about which one to pick for my next track day. Any advice?   ![Image](/static/user_uploads/gt3_vs_rs.jpg)",
        "replies": [
            {"user_name": "mickey.mouse", "content": "The GT3 is an amazing all-rounder, but the RS is built to dominate on the track. If it’s purely for lap times, go with the RS."},
            {"user_name": "minnie.mouse", "content": "GT3RS has the edge in aerodynamics and downforce. If you love late braking and high-speed corners, that’s the one."},
            {"user_name": "donald.duck", "content": "The GT3 is more forgiving for novice track enthusiasts, but the RS really comes alive in skilled hands. What’s your experience level?"},
            {"user_name": "elsa", "content": "I’d choose the RS for its aggressive looks alone, but be prepared for a much harsher ride compared to the GT3."},
            {"user_name": "stitch", "content": "GT3RS might be faster, but the GT3 offers a better balance between track and occasional street use. Is it only for track days?"},
            {"user_name": "pluto", "content": "Have you considered tire wear and maintenance costs? The RS’s aggressive setup can be pricey to maintain after frequent track use."},
            {"user_name": "simba", "content": "The RS shines on tracks with long straights and fast corners. On a tighter circuit, the GT3 might be just as quick and easier to handle."},
            {"user_name": "anna", "content": "Do you care about the sound? Both are amazing, but the RS’s titanium exhaust has a rawness that’s hard to beat."},
            {"user_name": "daisy.duck", "content": "The RS’s aero package is designed to maximize grip, but it can be intimidating for a beginner. Are you comfortable with high-speed oversteer?"},
            {"user_name": "goofy", "content": "If you’re planning on competitive track days, the RS’s lap times will be worth it. Otherwise, the GT3 might give you more smiles per mile."}
        ]
    },
    {
        "title": "spyder demans engine vs sypder rs?",
        "content": "Spyder vs Spyder RS: Which one has the edge for spirited driving? Does the demans engine upgrade bring the regular spyder up to the rs's level?    ![Image](/static/user_uploads/demans.jpg)",
        "replies": [
            {"user_name": "mickey.mouse", "content": "The Spyder RS is a track-focused beast, but the Demans engine upgrade can make the standard Spyder a serious contender for spirited driving."},
            {"user_name": "minnie.mouse", "content": "If you’re mostly on twisty roads, the balance of the standard Spyder with the Demans engine might be more fun than the RS’s stiffer setup."},
            {"user_name": "donald.duck", "content": "The RS is unmatched for precision and adrenaline on the track, but the Demans upgrade makes the regular Spyder much more versatile for everyday driving."},
            {"user_name": "goofy", "content": "I’ve driven both, and the RS’s sound and responsiveness from the GT3-derived engine are on another level. The Demans is powerful but lacks that theater."},
            {"user_name": "daisy.duck", "content": "The Spyder RS feels raw and alive, while the Demans upgrade smooths out the power delivery for a more refined experience. What kind of driving do you prefer?"},
            {"user_name": "stitch", "content": "The Demans engine adds great performance, but it doesn’t quite match the downforce and cornering capability of the RS. Is weight reduction a factor for you?"},
            {"user_name": "pluto", "content": "The RS’s lighter body and sharper handling make a huge difference on mountain roads. The Spyder with Demans is great, but it’s not as razor-sharp."},
            {"user_name": "simba", "content": "The RS is for those who want a hardcore experience, but the Demans upgrade offers better value for a daily driver with spirited capabilities."},
            {"user_name": "elsa", "content": "With the RS, you get GT3-level excitement, but the Demans engine closes the gap enough to make it hard to justify the price difference for most people."},
            {"user_name": "anna", "content": "Unless you’re pushing the car to its limits on the track, the standard Spyder with Demans feels just as thrilling and a bit more forgiving."
            }
        ]
    },
]




LUCID_POSTS = [
    {
        "title": "Lucid Air Performance on Long Trips",
        "content": "Took the Lucid Air on a 500-mile road trip. The range and comfort are outstanding!   ![Image](/static/user_uploads/lucid_trip.jpg)",
        "replies": [
            {"user_name": "mickey.mouse", "content": "500 miles! That’s impressive. How was the charging experience on the trip?"},
            {"user_name": "elsa", "content": "Lucid’s tech is amazing. Did you notice any battery degradation over long stretches?"},
        ],
    },
    {
        "title": "Lucid vs Tesla: Which is better?",
        "content": "I’m torn between the Lucid Air and Tesla Model S. Any thoughts?   ![Image](/static/user_uploads/lucid_vs_tesla.jpg)",
        "replies": [
            {"user_name": "donald.duck", "content": "The Lucid Air has better interior quality, but Tesla’s charging network is unbeatable."},
            {"user_name": "minnie.mouse", "content": "For tech and range, the Lucid Air wins. But Tesla has the autopilot edge."},
        ],
    },
]




# Sample Disney users with profile picture filenames
DISNEY_USERS = [
    ("mickey.mouse", "mickey@disney.com", "Mickey Mouse", "Toontown"),
    ("minnie.mouse", "minnie@disney.com", "Minnie Mouse", "Toontown"),
    ("donald.duck", "donald@disney.com", "Donald Duck", "Duckburg"),
    ("goofy", "goofy@disney.com", "Goofy", "Goofy Town"),
    ("pluto", "pluto@disney.com", "Pluto", "Toontown"),
    ("daisy.duck", "daisy@disney.com", "Daisy Duck", "Duckburg"),
    ("elsa", "elsa@disney.com", "Elsa", "Arendelle"),
    ("anna", "anna@disney.com", "Anna", "Arendelle"),
    ("simba", "simba@disney.com", "Simba", "Pride Lands"),
    ("stitch", "stitch@disney.com", "Stitch", "Hawaii"),
]

# Directory for profile pictures
PFP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../forum/static/pfp')

def insert_users():
    """Insert users and their profile pictures into the database."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor()

            # Clear existing data
            print("Truncating tables...")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            cursor.execute("TRUNCATE TABLE UserProfile;")
            cursor.execute("TRUNCATE TABLE User;")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

            # Insert users
            print("Inserting users...")
            for user_name, email, profile_name, location in DISNEY_USERS:
                # Insert into User table
                cursor.execute("""
                    INSERT INTO User (user_name, registration_date, email, password)
                    VALUES (%s, %s, %s, %s)
                """, (user_name, datetime.now(), email, "Password123!"))

                # Determine avatar path in the format: ![Image](/static/pfp/filename)
                avatar_filename = f"{user_name}.jpg"
                avatar_full_path = os.path.join(PFP_DIR, avatar_filename)
                if os.path.exists(avatar_full_path):
                    avatar_path = f"![Image](/static/pfp/{avatar_filename})"
                else:
                    avatar_path = "![Image](/static/pfp/default.jpg)"

                # Insert into UserProfile table
                cursor.execute("""
                    INSERT INTO UserProfile (user_name, avatar, location)
                    VALUES (%s, %s, %s)
                """, (user_name, avatar_path, location))

            connection.commit()
            print("Users and profile pictures inserted successfully.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Function to insert images into the database
def insert_images(cursor):
    """
    Insert image filenames and their tags into the database.
    """
    print("Inserting images into the database...")
    for filename, tags in IMAGES_AND_TAGS.items():
        file_path = os.path.join(UPLOADS_DIR, filename)
        if os.path.exists(file_path):
            # Insert the filename into the Image table
            cursor.execute("""
                INSERT INTO Image (filename)
                VALUES (%s)
            """, (filename,))
            image_id = cursor.lastrowid

            # Insert tags into the ImageSubjects table
            for tag in tags:
                cursor.execute("""
                    INSERT INTO ImageSubjects (image_id, subject)
                    VALUES (%s, %s)
                """, (image_id, tag))
        else:
            print(f"Warning: File {filename} not found in {UPLOADS_DIR}")



# Main data insertion logic
def insert_data():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor()

            # Truncate tables to clear existing data
            print("Truncating tables...")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            cursor.execute("TRUNCATE TABLE ImageSubjects;")
            cursor.execute("TRUNCATE TABLE Image;")
            cursor.execute("TRUNCATE TABLE Post;")
            cursor.execute("TRUNCATE TABLE Topic;")
            cursor.execute("TRUNCATE TABLE Overboard;")
            cursor.execute("TRUNCATE TABLE UserProfile;")
            cursor.execute("TRUNCATE TABLE User;")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

            # Insert images
            insert_images(cursor)

            # Insert users
            insert_users()



            print("Inserting overboards and topics...")
            post_creators = ["donald.duck", "mickey.mouse", "minnie.mouse", "elsa"]
            creator_index = 0  # To alternate creators

            for board_name, topics in TOPICS.items():
                # Insert overboard
                cursor.execute("""
                    INSERT INTO Overboard (name, description)
                    VALUES (%s, %s)
                """, (board_name, f"Discussion about {board_name.lower()}"))
                overboard_id = cursor.lastrowid

                for topic_title in topics:
                    # Insert topic
                    cursor.execute("""
                        INSERT INTO Topic (overboard_id, created_by, title, creation_date)
                        VALUES (%s, %s, %s, %s)
                    """, (overboard_id, post_creators[creator_index], topic_title, datetime.now()))
                    topic_id = cursor.lastrowid
                    creator_index = (creator_index + 1) % len(post_creators)  # Alternate creators

                    # Dynamically determine post set to use based on topic
                    post_set_name = f"{topic_title.upper()}_POSTS" 
                    posts_to_insert = globals().get(post_set_name, []) 

                    if posts_to_insert:
                        print(f"Inserting posts under topic {topic_title} ({topic_id})...")
                        for post in posts_to_insert:
                            # Insert main post
                            cursor.execute("""
                                INSERT INTO Post (topic_id, user_name, content, post_date, reply_to_post_id)
                                VALUES (%s, %s, %s, %s, NULL)
                            """, (topic_id, post_creators[creator_index], post["content"], datetime.now()))
                            post_id = cursor.lastrowid
                            creator_index = (creator_index + 1) % len(post_creators)  # Alternate creators

                            # Insert replies for the post
                            for reply in post["replies"]:
                                cursor.execute("""
                                    INSERT INTO Post (topic_id, user_name, content, post_date, reply_to_post_id)
                                    VALUES (%s, %s, %s, %s, %s)
                                """, (topic_id, reply["user_name"], reply["content"], datetime.now(), post_id))


            connection.commit()
            print("Database reset and populated successfully.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    insert_data()
