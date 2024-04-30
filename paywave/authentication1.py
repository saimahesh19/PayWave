import mysql.connector
import bcrypt

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



def authenticate_user(conn, UserID, Password):
    try:
        cursor = conn.cursor()
        # Retrieve the hashed password for the provided UserID
        cursor.execute("SELECT Password FROM users WHERE UserID = %s", (UserID,))
        user_data = cursor.fetchone()
        
        if user_data:
            hashed_password = user_data[0].encode('utf-8')
            # Check if the provided password matches the stored hashed password
            if bcrypt.checkpw(Password.encode('utf-8'), hashed_password):
                print("Authentication successful. Welcome,", UserID)
            else:
                print("Authentication failed. Incorrect password.")
        else:
            print("Authentication failed. User not found.")
    except mysql.connector.Error as err:
        print("Error during authentication:", err)

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

    # Authenticate the user
    authenticate_user(conn, UserID, Password)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()
