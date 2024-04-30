# import mysql.connector
# import bcrypt

# def create_database_connection():
#     try:
#         # Replace 'your_mysql_username' and 'your_mysql_password' with your MySQL credentials
#         conn = mysql.connector.connect(
#             host='localhost',
#             user='root',
#             password='qwerty_123',
#             database='paywave'
#         )
#         return conn
#     except mysql.connector.Error as err:
#         print("Error connecting to MySQL:", err)
#         return None

# def create_users_table(conn):
#     try:
#         cursor = conn.cursor()
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 UserID VARCHAR(50) NOT NULL,
#                 Password VARCHAR(100) NOT NULL
#             )
#         """)
#         conn.commit()
#         print("Table 'users' created successfully.")
#     except mysql.connector.Error as err:
#         print("Error creating 'users' table:", err)

# def hash_password(password):
#     # Hash the password using bcrypt
#     salt = bcrypt.gensalt()
#     hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
#     return hashed_password.decode('utf-8')

# def insert_user(conn, UserID, Password):
#     try:
#         cursor = conn.cursor()
#         hashed_password = hash_password(Password)
#         sql = "INSERT INTO users (UserID, Password) VALUES (%s, %s)"
#         values = (UserID, hashed_password)
#         cursor.execute(sql, values)
#         conn.commit()
#         print("User data inserted successfully.")
#     except mysql.connector.Error as err:
#         print("Error inserting user data:", err)

# def main():
#     # Get user input
#     UserID = input("Enter UserID: ")
#     Password = input("Enter Password: ")

#     # Create a database connection
#     conn = create_database_connection()
#     if not conn:
#         return

#     # Create the 'users' table if it doesn't exist
#     create_users_table(conn)

#     # Insert the user data into the 'users' table
#     insert_user(conn, UserID, Password)

#     # Close the connection

#     conn.close()

# if __name__ == "__main__":
#     main()


import mysql.connector

def create_database_connection():
    try:
        # Replace 'your_mysql_username' and 'your_mysql_password' with your MySQL credentials
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='qwerty_123',
            database='paywave'
        )
        return conn
    except mysql.connector.Error as err:
        print("Error connecting to MySQL:", err)
        return None

def create_users_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                UserID VARCHAR(50) NOT NULL,
                Password VARCHAR(100) NOT NULL
            )
        """)
        conn.commit()
        print("Table 'users' created successfully.")
    except mysql.connector.Error as err:
        print("Error creating 'users' table:", err)

def insert_user(conn, UserID, Password):
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO users (UserID, Password) VALUES (%s, %s)"
        values = (UserID, Password)
        cursor.execute(sql, values)
        conn.commit()
        print("User data inserted successfully.")
    except mysql.connector.Error as err:
        print("Error inserting user data:", err)

def main():
    # Get user input
    UserID = input("Enter UserID: ")
    Password = input("Enter Password: ")

    # Create a database connection
    conn = create_database_connection()
    if not conn:
        return

    # Create the 'users' table if it doesn't exist
    create_users_table(conn)

    # Insert the user data into the 'users' table (without hashing the password)
    insert_user(conn, UserID, Password)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()
 