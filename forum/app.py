from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure random secret key

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '3kAF9saj!!!',
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
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title, overboard_id FROM Topic WHERE topic_id = %s", (topic_id,))
    topic = cursor.fetchone()
    topic_title = topic[0] if topic else "Unknown Topic"
    overboard_id = topic[1] if topic else None

    cursor.execute("SELECT post_id, user_name, content, post_date FROM Post WHERE topic_id = %s AND reply_to_post_id IS NULL", (topic_id,))
    posts = cursor.fetchall()

    # Pass overboard_id to the template
    return render_template('posts.html', topic_title=topic_title, posts=posts, overboard_id=overboard_id)


@app.route('/replies/<int:post_id>')
def replies(post_id):
    if 'user_id' not in session:
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT topic_id, content FROM Post WHERE post_id = %s", (post_id,))
    post = cursor.fetchone()
    if not post:
        return "Post not found", 404

    topic_id, original_content = post

    cursor.execute("SELECT user_name, content, post_date FROM Post WHERE reply_to_post_id = %s", (post_id,))
    replies = cursor.fetchall()

    # Pass post_id to the template
    return render_template(
        'replies.html', 
        original_content=original_content, 
        replies=replies, 
        topic_id=topic_id, 
        post_id=post_id
    )


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

    # Insert the reply into the Post table
    cursor.execute("""
        INSERT INTO Post (user_name, profile_id, overboard_id, topic_id, content, reply_to_post_id, post_date)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """, (user_name, profile_id, overboard_id, topic_id, content, post_id))
    conn.commit()

    # Redirect back to the replies page
    return redirect(url_for('replies', post_id=post_id))



@app.route('/logout')
def logout():
    # Clear session and redirect to login
    session.pop('user_id', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

