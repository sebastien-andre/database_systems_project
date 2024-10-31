import mysql.connector
from mysql.connector import Error

def create_connection():
    """Create a database connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='3kAF9saj!!!',  # Your actual MySQL password
        )
        if connection.is_connected():
            print("Successfully connected to MySQL.")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def execute_sql_file(connection, file_path):
    """Execute the SQL commands in the specified file."""
    cursor = connection.cursor()
    with open(file_path, 'r') as file:
        sql_script = file.read()
    try:
        cursor.execute(sql_script, multi=True)
        print("SQL script executed successfully.")
    except Error as e:
        print(f"Error executing SQL script: {e}")

def main():
    """Main function to create connection and run SQL script."""
    connection = create_connection()
    if connection:
        execute_sql_file(connection, 'setup.sql')
        connection.close()

if __name__ == "__main__":
    main()
