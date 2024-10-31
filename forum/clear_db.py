import mysql.connector

# Establish a connection to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="your_username",     # Replace with your MySQL username
    password="your_password", # Replace with your MySQL password
    database="your_database"  # Replace with your MySQL database name
)
cursor = conn.cursor()

# Disable foreign key checks to allow truncating tables that have foreign keys
cursor.execute('SET FOREIGN_KEY_CHECKS = 0')

# Truncate each table to remove all data but keep the structure intact
tables = ['Post', 'UserProfile', 'User', 'Topic', 'Overboard', 'ImageSubjects', 'Image', 'PostTags']

for table in tables:
    cursor.execute(f'TRUNCATE TABLE {table}')
    print(f"Table {table} has been cleared.")

# Re-enable foreign key checks
cursor.execute('SET FOREIGN_KEY_CHECKS = 1')

# Commit changes and close the connection
conn.commit()
conn.close()

print("All tables have been cleared.")
