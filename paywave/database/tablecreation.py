# import mysql.connector

# # Replace with your MySQL database connection parameters
# host='localhost'
# user='root'
# password='qwerty_123'
# database='paywave'

# # Create a MySQL database connection
# conn = mysql.connector.connect(
#     host=host,
#     user=user,
#     password=password,
#     database=database
# )

# # Create a cursor object to interact with the database
# cursor = conn.cursor()

# # # Define the SQL statements to create tables
# # create_user_table = """
# # CREATE TABLE IF NOT EXISTS user (
# #     user_id INT AUTO_INCREMENT PRIMARY KEY,
# #     username VARCHAR(255) NOT NULL,
# #     password VARCHAR(255) NOT NULL,
# #     email VARCHAR(255) NOT NULL,
# #     balance FLOAT DEFAULT 0.0
# # )
# # """

# # create_transaction_history_table = """
# # CREATE TABLE IF NOT EXISTS transaction_history (
# #     transaction_id INT AUTO_INCREMENT PRIMARY KEY,
# #     user_id INT NOT NULL,
# #     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
# #     amount FLOAT NOT NULL,
# #     description TEXT,
# #     qr_code_info TEXT,
# #     FOREIGN KEY (user_id) REFERENCES user (user_id)
# # )
# # """

# # # Execute the SQL statements to create tables
# # cursor.execute(create_user_table)
# # cursor.execute(create_transaction_history_table)
# create_table_query = """
#         CREATE TABLE IF NOT EXISTS history (
#             transaction_id INT AUTO_INCREMENT PRIMARY KEY,
#             user_id INT,
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#             amount FLOAT NOT NULL,
#             status TEXT,
#             url TEXT,
#             balance DECIMAL(10, 2) DEFAULT 0.00,
#             payment_status VARCHAR(10) NOT NULL
#         )
#         """
# cursor.execute(create_table_query)
# # Commit the changes and close the database connection
# conn.commit()
# conn.close()



import mysql.connector
import cv2
from pyzbar.pyzbar import decode
import urllib.parse
import re
import requests
import certifi
import tldextract
import joblib
import datetime

# Replace 'YOUR_API_KEY' with your actual VirusTotal API key
api_key = '42a1ce328eacf3efacc042b8c2fb170d944a4662fb2ea7fca75f08164e023ae9'

# Define a global variable to store the username of the logged-in user
logged_in_username = None

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
# Function for the paywave functionality




# Function for checking balance
def balance():
    global logged_in_username  # Access the logged-in username
    print(f"This is the balance of {logged_in_username}")
    # Your balance checking logic goes here

# Inside the scan_qr function
def scan_qr():
    global logged_in_username  # Access the logged-in username
    print(f"This is the scan function of {logged_in_username}")
    
    # Scan QR code and save URL to scanned_url.txt
    scanned_url = scan_qr_code()
    url_test = 1
    certificate_test = 1
    structure_test = 1
    tld_test = 1
    virus_total_test = 1
    status = "failed"

    # Initialize count variable to track non-malicious test cases
    count = 0

    # Test URL for maliciousness
    if test_url(scanned_url):
        count += 1
        print("test 1 ")
        url_test = 0
    # Analyze URL structure
    analyze_result = analyze_url_structure(scanned_url)
    if analyze_result == "Normal":
        count += 1
        print("test 2")
        structure_test = 0
    # Validate SSL certificate for the URL
    if validate_certificate(scanned_url):
        count += 1
        print("test 3")
        certificate_test = 0
    # Check website reputation using VirusTotal API
    reputation, total_scanners = check_website_reputation(scanned_url)
    if reputation == 0:
        count += 1
        print("test 4 ")
        virus_total_test = 0
    # Validate TLD for the URL
    tld_result = validate_tld(scanned_url)
    if tld_result == "Valid TLD":
        count += 1
        print("test 5")
        tld_test = 0
    print(count)
    # Check if count is 5 (all non-malicious tests passed)
    if count == 5:
        print("Your QR code is safe to use.")
        proceed_payment(logged_in_username, scanned_url)
    else:
        print("Your QR code may be suspicious. Proceed with caution.")
    
    # Check if all tests passed
    if url_test == 0 and certificate_test == 0 and structure_test == 0 and tld_test == 0 and virus_total_test == 0:
        status = "success"

    # Update the database table 'test_table' with test results
    update_test_table(logged_in_username, scanned_url, url_test, certificate_test, structure_test, tld_test, virus_total_test, status)

    # Print the results
    print(f"URL Test: {url_test}")
    print(f"Certificate Test: {certificate_test}")
    print(f"structure_test: {structure_test}")
    print(f"TLD Test: {tld_test}")
    print(f"VirusTotal Test: {virus_total_test}")
    print(f"Status: {status}")


# Function to update the 'test_table' in the database
def update_test_table(username, url, url_test, certificate_test, structure_test, tld_test, virus_total_test, status):
    db = connect_to_database()
    cursor = db.cursor()
    
    # SQL query to insert/update a row in the 'test_table'
    query = """
    INSERT INTO test_table (user_id, url, url_test, certificate_test, structure_test, tld_test, virus_total_test, status)
    VALUES ((SELECT user_id FROM user WHERE username = %s), %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    url_test = VALUES(url_test),
    certificate_test = VALUES(certificate_test),
    structure_test = VALUES(structure_test),
    tld_test = VALUES(tld_test),
    virus_total_test = VALUES(virus_total_test),
    status = VALUES(status)
    """
    
    # Execute the query with parameters
    cursor.execute(query, (username, url, url_test, certificate_test, structure_test, tld_test, virus_total_test, status))
    
    # Commit the changes to the database
    db.commit()


# Function to scan QR code and save URL to scanned_url.txt
def scan_qr_code():
    cap = cv2.VideoCapture(0)  # Use the default camera (index 0) or specify the camera device
    
    while True:
        _, frame = cap.read()
        qr_codes = decode(frame)
        
        if qr_codes:
            qr_code = qr_codes[0]
            url = qr_code.data.decode('utf-8')
            print("Scanned URL:", url)
            with open("scanned_url.txt", "w") as f:
                f.write(url)
            cap.release()
            cv2.destroyAllWindows()
            return url
        
        cv2.imshow("QR Code Scanner", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Rest of your code...
# Function to test URL for maliciousness
def test_url(url):
    # Preprocess the URL
    url = preprocess(url)

    # Load the trained model from the "url.joblib" file
    model_filename = r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem5\prj\securecoding\cds\url.joblib"
    loaded_model = joblib.load(model_filename)

    # Predict the label for the URL using the loaded model
    label = loaded_model.predict([url])[0]

    # Output the result and label
    result = "False Positive" if label == 0 else "True Positive"
    print(f"The classification result is: {result}")
    print(f"The predicted label is: {label}")

    # Check if it's a non-malicious result and update the count
    if label == "benign":
        return True
    else:
        return False

# Function to analyze URL structure
def analyze_url_structure(url):
    parsed_url = urllib.parse.urlparse(url)
    
    # Check for anomalies in the URL structure
    if len(parsed_url.netloc) > 50:
        return "Suspicious"  # Long domain or subdomain
    
    return "Normal"  # No anomalies detected

# Function to validate SSL certificate for a given URL
def validate_certificate(url):
    try:
        # Send a GET request to the URL with certifi's CA bundle
        response = requests.get(url, timeout=5, verify=certifi.where())
        
        # Check if the response has a valid SSL certificate
        if response.status_code == 200:
            print(f"Certificate for {url} is valid and trusted.")
            return True
        else:
            print(f"Failed to retrieve the URL. May not be allowed for payment.")
            return False
    
    except requests.exceptions.RequestException as e:
        print("Failed to retrieve the URL. May not be allowed for payment.")
        return False

# Function to check website reputation using VirusTotal API
def check_website_reputation(url):
    try:
        # VirusTotal API endpoint for URL scanning
        url_scan_url = f'https://www.virustotal.com/vtapi/v2/url/scan'
        
        # VirusTotal API endpoint for retrieving scan reports
        report_url = f'https://www.virustotal.com/vtapi/v2/url/report'

        # Parameters for URL scanning
        params = {'apikey': api_key, 'url': url}
        
        # Submit the URL for scanning
        response = requests.post(url_scan_url, data=params)
        scan_result = response.json()

        # Check if the URL scan was successful
        if scan_result.get('response_code') == 1:
            scan_id = scan_result.get('scan_id')
            
            # Retrieve the scan report
            params = {'apikey': api_key, 'resource': scan_id}
            report_response = requests.get(report_url, params=params)
            report_data = report_response.json()
            
            # Extract the reputation score and scan results
            reputation = report_data.get('positives', 0)
            total_scanners = report_data.get('total', 0)

            # Display the results
            print(f'Reputation Score: {reputation}/{total_scanners}')
            print('Scan Results:')
            
            # Check if it's a non-malicious result and update the count
            if reputation == 0:
                return 0, total_scanners
            else:
                return reputation, total_scanners

        else:
            print('URL scan failed. Check the URL or try again later.')
            return 0, 0  # Return 0 reputation and total_scanners on failure

    except Exception as e:
        print(f'Error: {e}')
        return 0, 0  # Return 0 reputation and total_scanners on error

# Function to validate TLD (Top-Level Domain)
def validate_tld(url):
    extracted = tldextract.extract(url)
    tld = extracted.suffix
    
    # List of trusted TLDs (add more if needed)
    trusted_tlds = ["com", "org", "net", "edu"]
    
    if tld in trusted_tlds:
        return "Valid TLD"
    else:
        return "Suspicious TLD"

# Preprocessing function
def preprocess(url):
    # Parse the URL
    url = urllib.parse.unquote(url)
    url = url.lower()
    # Remove http and www
    url = re.sub(r'^https?://(?:www\.)?', '', url)
    # Remove trailing slash
    url = re.sub(r'/$', '', url)
    return url


def paywave():
    global logged_in_username  # Access the logged-in username
    print("Welcome to Paywave")
    
    while True:
        print("1. Check Balance")
        print("2. Scan QR for Payment")
        print("3. Deposit Money")
        print("4. Transaction History")
        print("5. Logout")
        user_choice = input("Enter your choice: ")

        if user_choice == "1":
            balance()
        elif user_choice == "2":
            scan_qr()
        elif user_choice == "3":
            deposit_money()
        elif user_choice == "4":
            transaction_history()
        elif user_choice == "5":
            logged_in_username = None  # Clear the logged-in username
            break
        else:
            print("Invalid choice. Please select a valid option.")
    
    # # Check if count is 5 (all non-malicious tests passed)
    # if count == 5:
    #     proceed_payment(logged_in_username)

# Function to display transaction history
def transaction_history():
    global logged_in_username  # Access the logged-in username
    
    try:
        db = connect_to_database()
        cursor = db.cursor()
        query = "SELECT * FROM history WHERE user_id = (SELECT user_id FROM user WHERE username = %s) ORDER BY transaction_id DESC"
        cursor.execute(query, (logged_in_username,))
        transactions = cursor.fetchall()

        if transactions:
            print("Transaction History:")
            print("{:<10} {:<20} {:<30} {:<10} {:<10} {:<10}".format("Transaction ID", "Timestamp", "URL", "Amount", "Status", "Balance"))
            for transaction in transactions:
                print("{:<15} {:<20} {:<30} {:<10} {:<10} {:<10}".format(transaction[0], transaction[1], transaction[2], transaction[3], transaction[4], transaction[6]))
        else:
            print("No transaction history available.")
    except Exception as e:
        print(f"Failed to retrieve transaction history: {e}")
    finally:
        db.close()
# Function to proceed with payment
def proceed_payment(username, scanned_url):
    global logged_in_username  # Access the logged-in username
    print(f"Proceeding with payment for {username}")

    try:
        db = connect_to_database()
        cursor = db.cursor()
        
        # Fetch the user's current balance and user_id
        query = "SELECT user_id, balance FROM user WHERE username = %s"
        cursor.execute(query, (logged_in_username,))
        user_result = cursor.fetchone()

        if user_result:
            user_id = user_result[0]  # Retrieve user_id as an integer
            current_balance = user_result[1]
            print(f"Your current balance is: ${current_balance:.2f}")

            # Prompt the user to enter the payment amount
            payment_amount = float(input("Enter the payment amount: $"))

            # Check if the user has sufficient balance for the payment
            if payment_amount <= 0:
                print("Invalid amount. Please enter a positive amount to pay.")
            elif payment_amount > current_balance:
                print("Payment failed. Insufficient balance.")
            else:
                # Update the user's balance after successful payment
                new_balance = current_balance - payment_amount
                update_query = "UPDATE user SET balance = %s WHERE username = %s"
                cursor.execute(update_query, (new_balance, logged_in_username))
                db.commit()
                print(f"Payment of ${payment_amount:.2f} successful. Your new balance is: ${new_balance:.2f}")

                # Store the transaction history
                store_transaction_history(user_id, scanned_url, payment_amount, "success")
        else:
            print("Failed to retrieve user information.")

    except ValueError:
        print("Invalid input. Please enter a valid payment amount.")
    finally:
        db.close()

# Function to store transaction history
# Function to store transaction history
def store_transaction_history(user_id, scanned_url, amount, status):
    try:
        db = connect_to_database()
        cursor = db.cursor()

        # Fetch the user's current balance from the user table
        balance_query = "SELECT balance FROM user WHERE user_id = %s"
        cursor.execute(balance_query, (user_id,))
        balance_result = cursor.fetchone()

        if balance_result:
            current_balance = balance_result[0]

            # Insert the transaction history record
            insert_query = """
                INSERT INTO history (user_id, timestamp, amount, status, url, balance, payment_status)
                VALUES (%s, NOW(), %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (user_id, amount, status, scanned_url, current_balance, "success"))
            db.commit()
            print("Transaction history stored successfully.")
        else:
            print("Failed to retrieve the user's balance.")

    except Exception as e:
        print(f"Failed to store transaction history: {e}")
    finally:
        db.close()



# Function for depositing money
def deposit_money():
    global logged_in_username  # Access the logged-in username
    try:
        deposit_amount = float(input("Enter the amount to deposit: $"))
        if deposit_amount <= 0:
            print("Invalid amount. Please enter a positive amount to deposit.")
            return

        db = connect_to_database()
        cursor = db.cursor()
        query = "UPDATE user SET balance = balance + %s WHERE username = %s"
        cursor.execute(query, (deposit_amount, logged_in_username))
        db.commit()
        print(f"${deposit_amount:.2f} deposited successfully.")
        db.close()
    except ValueError:
        print("Invalid input. Please enter a valid amount.")

# Function for checking balance
def balance():
    global logged_in_username  # Access the logged-in username
    db = connect_to_database()
    cursor = db.cursor()
    query = "SELECT balance FROM user WHERE username = %s"
    cursor.execute(query, (logged_in_username,))
    balance_result = cursor.fetchone()

    if balance_result:
        print(f"Your current balance is: ${balance_result[0]:.2f}")
    else:
        print("Failed to retrieve balance information.")
    db.close()


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

# def create_history_table():
#     try:
#         db = connect_to_database()
#         cursor = db.cursor()
#         create_table_query = """
#         CREATE TABLE IF NOT EXISTS history (
#             transaction_id INT AUTO_INCREMENT PRIMARY KEY,
#             user_id INT,
#             timestamp DATETIME,
#             url TEXT,
#             amount FLOAT,
#             status VARCHAR(255)
#         )
#         """
#         cursor.execute(create_table_query)
#         db.commit()
#         print("History table created successfully.")
#     except Exception as e:
#         print(f"Error creating history table: {e}")
#     finally:
#         db.close()

# # Add this line to create the 'history' table when the script is run
# create_history_table()