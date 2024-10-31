from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a random secret key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '3kAF9saj!!!',
    'database': 'forum'
}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM User WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]  # Store user ID in session
            return redirect(url_for('overboards'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('home'))

    except mysql.connector.Error as e:
        return f"Error: {e}"

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/overboards')
def overboards():
    if 'user_id' not in session:
        return redirect(url_for('home'))  # Redirect if not logged in

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute("SELECT overboard_id, name FROM Overboard")
        overboards = cursor.fetchall()
        return render_template('overboard.html', overboards=overboards)

    except mysql.connector.Error as e:
        return f"Error: {e}"

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/topics/<int:overboard_id>')
def topics(overboard_id):
    if 'user_id' not in session:
        return redirect(url_for('home'))  # Redirect if not logged in

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM Overboard WHERE overboard_id = %s", (overboard_id,))
        overboard_title = cursor.fetchone()

        cursor.execute("SELECT topic_id, overboard_id, title FROM Topic WHERE overboard_id = %s", (overboard_id,))
        topics = cursor.fetchall()

        return render_template('topic.html', overboard_title=overboard_title[0], topics=topics)

    except mysql.connector.Error as e:
        return f"Error: {e}"

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user from session
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
