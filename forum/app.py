from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import os
import base64
from datetime import datetime  
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'forum'
}

# Helper function to get database connection
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


@app.route('/')
def home():
    # Render the login page
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE user_name = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    # Check if user exists and login is valid
    if user:
        session['user_id'] = user[0]  # Store user ID in session
        return redirect(url_for('overboards'))
    else:
        flash("Invalid username or password")
        return redirect(url_for('home'))


@app.route('/overboards')
def overboards():
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT overboard_id, name, description FROM Overboard")
    overboards = cursor.fetchall()

    # Render the overboard page with overboard data
    return render_template('overboard.html', overboards=overboards)


@app.route('/topics/<int:overboard_id>')
def topics(overboard_id):
    print("Rendering topics for overboard ID:", overboard_id)
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM Overboard WHERE overboard_id = %s", (overboard_id,))
    overboard = cursor.fetchone()
    overboard_title = overboard[0] if overboard else "Unknown Overboard"

    cursor.execute("SELECT topic_id, title, created_by FROM Topic WHERE overboard_id = %s", (overboard_id,))
    topics = cursor.fetchall()

    # Render topic.html with the overboard title and list of topics
    return render_template('topic.html', overboard_title=overboard_title, topics=topics)


@app.route('/posts/<int:topic_id>')
def posts(topic_id):
    if 'user_id' not in session:
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the topic title and overboard ID
    cursor.execute("SELECT title, overboard_id FROM Topic WHERE topic_id = %s", (topic_id,))
    topic = cursor.fetchone()
    topic_title = topic[0] if topic else "Unknown Topic"
    overboard_id = topic[1] if topic else None

    # Fetch the total number of posts for this topic
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Post 
        WHERE topic_id = %s
    """, (topic_id,))
    total_posts = cursor.fetchone()[0]

    # Fetch posts for the topic
    cursor.execute("""
        SELECT 
            Post.post_id, Post.user_name, Post.content, Post.post_date, Image.filename 
        FROM Post 
        LEFT JOIN Image ON Post.image_id = Image.image_id 
        WHERE Post.topic_id = %s AND Post.reply_to_post_id IS NULL
    """, (topic_id,))
    posts = cursor.fetchall()

    conn.close()
    return render_template(
        'posts.html', 
        topic_title=topic_title, 
        posts=posts, 
        overboard_id=overboard_id, 
        topic_id=topic_id, 
        total_posts=total_posts
    )




@app.route('/replies/<int:post_id>')
def replies(post_id):
    if 'user_id' not in session:
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the original post and topic information
    cursor.execute("SELECT content, user_name, topic_id FROM Post WHERE post_id = %s", (post_id,))
    original_post = cursor.fetchone()

    if not original_post:
        return "Post not found", 404

    original_content, original_user, topic_id = original_post

    # Fetch all replies to the post
    cursor.execute("SELECT user_name, content, post_date, post_id FROM Post WHERE reply_to_post_id = %s", (post_id,))
    replies = cursor.fetchall()

    conn.close()

    return render_template(
        'replies.html',
        original_content=original_content,
        original_user=original_user,
        replies=replies,
        topic_id=topic_id,
        post_id=post_id
    )



@app.route('/delete_reply/<int:reply_id>', methods=['POST'])
def delete_reply(reply_id):
    if 'user_id' not in session:
        return redirect(url_for('home'))

    user_name = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the reply exists and belongs to the user
    cursor.execute("SELECT user_name FROM Post WHERE post_id = %s", (reply_id,))
    reply = cursor.fetchone()

    if not reply:
        flash("Reply not found.")
        return redirect(request.referrer)

    if reply[0] != user_name:
        flash("You are not authorized to delete this reply.")
        return redirect(request.referrer)

    # Delete the reply
    cursor.execute("DELETE FROM Post WHERE post_id = %s", (reply_id,))
    conn.commit()
    flash("Reply deleted successfully.")

    return redirect(request.referrer)




@app.route('/add_reply/<int:post_id>', methods=['POST'])
def add_reply(post_id):
    if 'user_id' not in session:
        return redirect(url_for('home'))

    content = request.form['content']
    user_name = session.get('user_id')  # Get the logged-in user
    profile_id = None  # Assuming you can fetch or set this based on the logged-in user

    # Fetch topic_id and overboard_id of the original post
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT topic_id, overboard_id FROM Post WHERE post_id = %s", (post_id,))
    post = cursor.fetchone()
    if not post:
        return "Post not found", 404

    topic_id, overboard_id = post

    # Clean up the content (prevent duplicate or malformed URLs)
    content_lines = content.split(" ")
    cleaned_content = []
    for line in content_lines:
        if line.startswith("![Image](/static/uploads/") and line.endswith(".jpg)"):
            cleaned_content.append(line)
        else:
            cleaned_content.append(line.strip())
    final_content = " ".join(cleaned_content)

    # Insert the reply into the Post table
    cursor.execute("""
        INSERT INTO Post (user_name, profile_id, overboard_id, topic_id, content, reply_to_post_id, post_date)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """, (user_name, profile_id, overboard_id, topic_id, final_content, post_id))
    conn.commit()

    # Redirect back to the replies page
    return redirect(url_for('replies', post_id=post_id))



@app.route('/logout')
def logout():
    # Clear session and redirect to login
    session.pop('user_id', None)
    return redirect(url_for('home'))



UPLOAD_FOLDER = 'forum/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'user_id' not in session:
        return redirect(url_for('home'))

    if 'image' not in request.files or 'subjects' not in request.form:
        return "Invalid request", 400

    image_file = request.files['image']
    subjects = request.form['subjects']

    if image_file.filename == '':
        return "No selected file", 400

    try:
        # Save the image
        filename = image_file.filename
        upload_path = os.path.join(app.static_folder, 'uploads', filename)
        image_file.save(upload_path)

        # Insert image details into the database
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO Image (filename) VALUES (%s)", (filename,))
        image_id = cursor.lastrowid

        # Insert subjects into ImageSubjects table
        for subject in subjects.split(','):
            subject = subject.strip()
            cursor.execute("INSERT INTO ImageSubjects (image_id, subject) VALUES (%s, %s)", (image_id, subject))

        conn.commit()
        conn.close()

        return redirect(url_for('search_images_popup'))

    except Exception as e:
        print(f"Error while uploading image: {e}")
        return "Internal Server Error", 500



@app.route('/select_image/<int:image_id>', methods=['GET'])
def select_image(image_id):
    if 'user_id' not in session:
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Retrieve the image details
    cursor.execute("SELECT name, content FROM Image WHERE image_id = %s", (image_id,))
    image = cursor.fetchone()
    conn.close()

    if not image:
        flash('Image not found.')
        return redirect(url_for('search_images'))

    return render_template('select_image.html', image=image)





@app.route('/search_images_popup', methods=['GET'])
def search_images_popup():
    if 'user_id' not in session:
        return redirect(url_for('home'))

    query = request.args.get('query', '')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Adjust the query to fetch the filename
        cursor.execute("""
            SELECT Image.image_id, Image.filename, GROUP_CONCAT(ImageSubjects.subject SEPARATOR ', ') AS subjects 
            FROM Image 
            LEFT JOIN ImageSubjects ON Image.image_id = ImageSubjects.image_id 
            WHERE ImageSubjects.subject LIKE %s 
            GROUP BY Image.image_id
        """, (f"%{query}%",))
        results = cursor.fetchall()

        # Debugging
        print("Search results:", results)

        conn.close()

        return render_template('search_images_popup.html', images=results, query=query)

    except Exception as e:
        print(f"Error in search_images_popup: {e}")
        return "Internal Server Error", 500




@app.route('/view_profile/<user_name>')
def view_profile(user_name):
    if 'user_id' not in session:
        return redirect(url_for('home'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch user profile details
        cursor.execute("""
            SELECT User.user_name, User.email, UserProfile.avatar, UserProfile.location
            FROM User
            LEFT JOIN UserProfile ON User.user_name = UserProfile.user_name
            WHERE User.user_name = %s
        """, (user_name,))
        user = cursor.fetchone()

        if not user:
            return "User not found", 404

        # Extract the URL from the Markdown-style avatar path
        if user[2] and user[2].startswith("![Image]("):
            avatar_url = user[2][9:-1]  # Extract text between "![Image](" and ")"
        else:
            avatar_url = '/static/pfp/default.jpg'  # Fallback to default image

        # Pass user data to the template
        return render_template(
            'profile.html',
            user_name=user[0],
            email=user[1],
            avatar_url=avatar_url,
            location=user[3]
        )

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return "Internal Server Error", 500

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()







@app.route('/profile/<user_name>/upload_avatar', methods=['POST'])
def upload_avatar(user_name):
    if 'user_id' not in session or session['user_id'] != user_name:
        return redirect(url_for('home'))

    avatar = request.files.get('avatar')
    if not avatar:
        flash('No file selected.')
        return redirect(url_for('view_profile', user_name=user_name))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE UserProfile 
        SET avatar = %s 
        WHERE user_name = %s
    """, (avatar.read(), user_name))
    conn.commit()
    conn.close()

    flash('Avatar updated successfully.')
    return redirect(url_for('view_profile', user_name=user_name))



# Route to edit the avatar for the logged-in user
@app.route('/profile/edit_avatar', methods=['POST'])
def edit_avatar():
    if 'user_id' not in session:
        return redirect(url_for('home'))

    user_name = session['user_id']
    file = request.files.get('avatar')

    if file and file.filename:
        filename = secure_filename(file.filename)
        avatar_data = file.read()

        conn = get_db_connection()
        cursor = conn.cursor()

        # Update the avatar in the database
        cursor.execute("""
            UPDATE UserProfile SET avatar = %s WHERE user_name = %s
        """, (avatar_data, user_name))
        conn.commit()
        conn.close()

        flash("Avatar updated successfully.")
        return redirect(url_for('view_profile', user_name=user_name))

    flash("Failed to upload avatar.")
    return redirect(url_for('view_profile', user_name=user_name))






@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        location = request.form.get('location', 'Unknown')

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if username already exists
        cursor.execute("SELECT * FROM User WHERE user_name = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Username already exists. Please choose another.")
            return redirect(url_for('register'))

        # Insert new user into the database
        try:
            registration_date = datetime.now()  # Add registration date here
            cursor.execute("""
                INSERT INTO User (user_name, registration_date, email, password)
                VALUES (%s, %s, %s, %s)
            """, (username, registration_date, email, password))

            cursor.execute("""
                INSERT INTO UserProfile (user_name, location)
                VALUES (%s, %s)
            """, (username, location))

            conn.commit()
            flash("Registration successful! You can now log in.")
            return redirect(url_for('home'))
        except Exception as e:
            print(f"Error during registration: {e}")
            flash("An error occurred during registration. Please try again.")
        finally:
            conn.close()

    # Render the registration form
    return render_template('register.html')




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/create_post/<int:topic_id>', methods=['GET', 'POST'])
def create_post(topic_id):
    if 'user_id' not in session:
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Ensure the topic exists
    cursor.execute("SELECT overboard_id FROM Topic WHERE topic_id = %s", (topic_id,))
    topic = cursor.fetchone()
    if not topic:
        flash("Topic not found.")
        return redirect(url_for('overboards'))
    overboard_id = topic[0]

    # Handle form submission
    if request.method == 'POST':
        content = request.form.get('content')
        image_file = request.files.get('image')  # Handle the image upload
        user_name = session['user_id']

        # Check if the user exists
        cursor.execute("SELECT user_name FROM User WHERE user_name = %s", (user_name,))
        user = cursor.fetchone()
        if not user:
            flash("Invalid user. Please log in again.")
            return redirect(url_for('logout'))

        # Process the image file if provided
        if image_file and allowed_file(image_file.filename):
            # Ensure the upload directory exists
            upload_dir = os.path.join('forum/static/user_uploads')
            os.makedirs(upload_dir, exist_ok=True)

            # Secure the filename and save the image
            filename = secure_filename(image_file.filename)
            upload_path = os.path.join(upload_dir, filename)
            image_file.save(upload_path)

            # Append the image as Markdown to the content
            image_markdown = f" ![Image](/static/user_uploads/{filename})"
            content += image_markdown

        # Insert the post into the Post table
        cursor.execute("""
            INSERT INTO Post (user_name, profile_id, overboard_id, topic_id, content, image_id, post_date)
            VALUES (%s, NULL, %s, %s, %s, NULL, NOW())
        """, (user_name, overboard_id, topic_id, content))

        conn.commit()
        flash("Post created successfully!")
        return redirect(url_for('posts', topic_id=topic_id))

    # Render the create post form
    return render_template('create_post.html', topic_id=topic_id)





if __name__ == '__main__':
    app.run(debug=True)



