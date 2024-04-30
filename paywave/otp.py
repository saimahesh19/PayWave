import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='qwerty_123',
    database='paywave'
)

cursor = db.cursor()

def create_user():
    print("Welcome! Let's create a new account.")
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    confirm_password = input("Confirm your password: ")
    phone_number = input("Enter your phone number: ")

    if password != confirm_password:
        print("Passwords do not match. Please try again.")
        return

    # Insert user data into the database
    insert_query = "INSERT INTO user (username, password, phone_number) VALUES (%s, %s, %s)"
    data = (username, password, phone_number)

    try:
        cursor.execute(insert_query, data)
        db.commit()
        print("Account created successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()

def login():
    print("Welcome back! Please log in.")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Check if the username and password exist in the database
    select_query = "SELECT * FROM user WHERE username = %s AND password = %s"
    data = (username, password)

    cursor.execute(select_query, data)
    result = cursor.fetchone()

    if result:
        print("Welcome to PayWave!")
    else:
        print("Invalid username or password. Please try again.")

def main():
    while True:
        print("Choose an option:")
        print("1. Create a new account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_user()
        elif choice == "2":
            login()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please select a valid option.")

    db.close()

if __name__ == "__main__":
    main()
