import mysql.connector

# Function to establish a database connection
def connect_to_database():
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='qwerty_123',
        database='paywave'
    )

    return db

# Function for user authentication
def authenticate_user(username, password):
    global logged_in_username  # Store the logged-in username globally
    db = connect_to_database()
    cursor = db.cursor()
    query = "SELECT * FROM user WHERE username = %s"
    cursor.execute(query, (username,))
    user_data = cursor.fetchone()
    
    if user_data and user_data[2] == password:
        logged_in_username = username  # Set the logged-in username
        return True
    
    return False

# Function for new user registration
def register_user(username, password, email):
    db = connect_to_database()
    cursor = db.cursor()
    query = "INSERT INTO user (username, password, email) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, password, email))
    db.commit()

# Function for the paywave functionality
def paywave():
    global logged_in_username  # Access the logged-in username
    print("Welcome to Paywave")
    
    while True:
        print("1. Check Balance")
        print("2. Scan QR for Payment")
        print("3. Logout")
        user_choice = input("Enter your choice: ")

        if user_choice == "1":
            balance()
        elif user_choice == "2":
            scan_qr()
        elif user_choice == "3":
            logged_in_username = None  # Clear the logged-in username
            break
        else:
            print("Invalid choice. Please select a valid option.")

# Function for checking balance
def balance():
    global logged_in_username  # Access the logged-in username
    print(f"This is the balance of {logged_in_username}")
    # Your balance checking logic goes here

# Function for scanning QR code
def scan_qr():
    global logged_in_username  # Access the logged-in username
    print(f"This is the scan function of {logged_in_username}")
    # Your QR code scanning logic goes here

# Main program
if __name__ == "__main__":
    while True:
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if authenticate_user(username, password):
                paywave()  # Call the paywave function after successful authentication
            else:
                print("Authentication failed. Please try again.")
        elif choice == "2":
            username = input("Enter your new username: ")
            password = input("Enter your new password: ")
            email = input("Enter your email: ")
            register_user(username, password, email)
            print("Registration successful. You can now log in.")
        elif choice == "3":
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")