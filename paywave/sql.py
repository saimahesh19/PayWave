# import cv2
# from pyzbar.pyzbar import decode
# import pandas as pd
# import urllib.parse
# import re
# from sklearn.model_selection import train_test_split
# from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
# from sklearn.pipeline import Pipeline
# from sklearn.linear_model import LogisticRegression
# import requests
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.svm import SVC
# import mysql.connector

# # Connect to MySQL database
# db_connection = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='qwerty_123',
#     database='paywave'
# )

# # Load the URL dataset
# df = pd.read_csv(r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem5\prj\securecoding\urldata.csv")

# # Preprocessing function
# def preprocess(url):
#     url = urllib.parse.unquote(url)
#     url = url.lower()
#     url = re.sub(r'^https?://(?:www\.)?', '', url)
#     url = re.sub(r'/$', '', url)
#     return url

# # Preprocess the URLs in the dataset
# df['url'] = df['url'].apply(preprocess)

# # Split the dataset into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(df['url'], df['label'], test_size=0.2)

# # Define the pipeline
# pipeline = Pipeline([
#     ('vect', CountVectorizer()),
#     ('tfidf', TfidfTransformer()),
#     ('clf', LogisticRegression())
# ])

# # Train the pipeline
# pipeline.fit(X_train, y_train)

# # Function to check if a URL is malicious
# def is_malicious(url):
#     url = preprocess(url)
#     label = pipeline.predict([url])[0]
#     return label == 1

# # Function to retrieve website source code
# def get_website_code(url):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             return response.text
#         else:
#             return f"Error: {response.status_code}"
#     except requests.exceptions.RequestException as e:
#         return f"Error: {e}"

# # Function to detect XSS vulnerabilities
# def detect_xss(code):
#     # Load the XSS dataset
#     dataset = pd.read_csv(r"C:\\Users\\SAI MAHESH\\Desktop\\files\\cipher game\\XSS_dataset.csv")
    
#     # Prepare the data
#     X = dataset['Payload']
#     y = dataset['Label']
    
#     # Create TF-IDF vectorizer
#     vectorizer = TfidfVectorizer()
    
#     # Transform the data
#     X = vectorizer.fit_transform(X)
    
#     # Train the SVM classifier
#     svm = SVC(kernel='linear')
#     svm.fit(X, y)
    
#     # Transform the website code using the same vectorizer
#     code_vector = vectorizer.transform([code])
    
#     # Predict the label for the website code
#     prediction = svm.predict(code_vector)
    
#     # Print the XSS prediction result
#     if prediction[0] == 1:
#         print("XSS vulnerability detected!")
#         return True
#     else:
#         print("No XSS vulnerability detected.")
#         return False

# # Function to scan QR code, check if it's malicious, and detect XSS vulnerabilities
# def scan_malicious_and_check_xss():
#     cap = cv2.VideoCapture(0)

#     while True:
#         _, frame = cap.read()
#         qr_codes = decode(frame)

#         if qr_codes:
#             qr_code = qr_codes[0]
#             url = qr_code.data.decode('utf-8')
#             print("Scanned URL:", url)
            
#             is_mal = is_malicious(url)
#             is_xss_detected = False
#             status = "Pending"
#             money = None
            
#             if not is_mal:
#                 print("URL is not malicious. Retrieving source code...")
#                 website_code = get_website_code(url)
#                 print("Website Source Code:\n", website_code)
                
#                 # Detect XSS vulnerability
#                 is_xss_detected = detect_xss(website_code)
#                 if not is_xss_detected:
#                     money = float(input("Enter transaction amount: "))
#                     status = "Completed"
#                 else:
#                     status = "Failed due to XSS vulnerability"
#             else:
#                 status = "Failed due to malicious URL"
            
#             # Insert transaction data into database
#             cursor = db_connection.cursor()
#             insert_query = "INSERT INTO TransactionHistory (url, is_malicious, is_xss, money, status) VALUES (%s, %s, %s, %s, %s)"
#             data = (url, is_mal, is_xss_detected, money, status)
#             cursor.execute(insert_query, data)
#             db_connection.commit()
            
#             print("Transaction recorded in database.")
            
#             break

#         cv2.imshow("QR Code Scanner", frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# # Call the QR code scanning and XSS checking function
# scan_malicious_and_check_xss()

# # Close database connection
# db_connection.close()
# _____________________________________________________


import mysql.connector
import cv2
from pyzbar.pyzbar import decode
import urllib.parse
import re
import joblib
import requests

# Load the saved SVM model and the fitted TF-IDF vectorizer for XSS detection
xss_model = joblib.load('xss_detection_model.joblib')
vectorizer = joblib.load('tfidf_vectorizer.joblib')

# Connect to MySQL
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='qwerty_123',
    database='paywave'
)

cursor = db.cursor()

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

# Function to test URL for maliciousness and retrieve source code
def test_url(scanned_url):
    # Preprocess the scanned URL
    url1 = scanned_url
    url = preprocess(scanned_url)

    # Load the trained model for URL classification
    model_filename = r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem5\prj\securecoding\cds\url.joblib"
    loaded_model = joblib.load(model_filename)

    # Predict the label for the scanned URL using the loaded model
    label = loaded_model.predict([url])[0]

    # Output the result and label
    result = "Benign" if label == 0 else "Malicious"
    print(f"The classification result is: {result}")
    print(f"The predicted label is: {label}")

    if label == "benign":
        extract_source_code(url1)
    else:
        print("No source code will be provided for malicious URLs.")

# Function to preprocess URL
def preprocess(url):
    # Parse the URL
    url = urllib.parse.unquote(url)
    url = url.lower()
    # Remove http and www
    url = re.sub(r'^https?://(?:www\.)?', '', url)
    # Remove trailing slash
    url = re.sub(r'/$', '', url)
    return url

# Function to check for XSS vulnerabilities in source code
def check_xss_vulnerability(source_code):
    input_vector = vectorizer.transform([source_code])
    prediction = xss_model.predict(input_vector)
    return prediction[0] == 1

# Function to extract source code of a URL if it's benign and check for XSS
def extract_source_code(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            source_code = response.text
            print("Source Code of the URL:")
            print(source_code)

            # Check for XSS vulnerability
            if check_xss_vulnerability(source_code):
                print("Potential XSS attack detected!")
            else:
                print("No XSS attack detected.")
        else:
            print("Unable to retrieve source code. HTTP Status Code:", response.status_code)
    except Exception as e:
        print("Error:", str(e))

# Function to create a new user account
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

# Function to authenticate the user
def authenticate_user():
    while True:
        print("Choose an option:")
        print("1. Create a new account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_user()
        elif choice == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if login(username, password):
                print("Authentication successful!")
                scanned_url = scan_qr_code()
                test_url(scanned_url)
            else:
                print("Authentication failed. Invalid username or password.")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please select a valid option.")

    db.close()

# Function to verify login credentials
def login(username, password):
    # Check if the username and password exist in the database
    select_query = "SELECT * FROM user WHERE username = %s AND password = %s"
    data = (username, password)

    cursor.execute(select_query, data)
    result = cursor.fetchone()

    return result is not None

if __name__ == "__main__":
    authenticate_user()
