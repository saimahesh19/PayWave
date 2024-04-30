from flask import Flask, request, jsonify
import mysql.connector
import cv2
from pyzbar.pyzbar import decode
import urllib.parse
import re
import requests
import certifi
import tldextract
import joblib
import pytz
import datetime
from flask_cors import CORS
app = Flask(__name__)
from flask import Response
import numpy as np
from flask_cors import cross_origin
CORS(app)

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
@app.route('/login', methods=['POST'])
def authenticate_user():
    global logged_in_username  # Store the logged-in username globally
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']

    db = connect_to_database()
    cursor = db.cursor()
    query = "SELECT * FROM user WHERE username = %s"
    cursor.execute(query, (username,))
    user_data = cursor.fetchone()

    if user_data and user_data[2] == password:
        logged_in_username = username  # Set the logged-in username
        return jsonify({'message': 'Authentication successful'}), 200
    else:
        return jsonify({'message': 'Authentication failed'}), 401

# Function for new user registration
@app.route('/register', methods=['POST'])
def register_user():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']
    email = request_data['email']

    db = connect_to_database()
    cursor = db.cursor()
    query = "INSERT INTO user (username, password, email) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, password, email))
    db.commit()

    return jsonify({'message': 'Registration successful'}), 201

@app.route('/balance', methods=['GET'])
def check_balance():
    global logged_in_username  # Access the logged-in username

    if logged_in_username is None:
        return jsonify({'message': 'User not logged in.'}), 401

    try:
        db = connect_to_database()
        cursor = db.cursor()
        query = "SELECT balance FROM user WHERE username = %s"
        cursor.execute(query, (logged_in_username,))
        balance_result = cursor.fetchone()

        if balance_result:
            balance_amount = balance_result[0]
            return jsonify({'message': f'Your current balance is: ${balance_amount:.2f}'}), 200
        else:
            return jsonify({'message': 'Failed to retrieve balance information.'}), 500
    except Exception as e:
        return jsonify({'message': f'Error: {e}'}), 500
    finally:
        db.close()


# Function to scan QR code and perform tests
@app.route('/scan_qr', methods=['POST'])
def scan_qr_endpoint():

    global logged_in_username  # Access the logged-in username


    

    # Check if the user is logged in
    if logged_in_username is None:
        return jsonify({'message': 'Not logged in.'}), 401

    
    request_data = request.get_json()
    qr_code = request_data['qr_code']


    request_data = request.get_json()
    scanned_url = request_data['scanned_url']

    # Initialize tests
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
        url_test = 0
    # Analyze URL structure
    analyze_result = analyze_url_structure(scanned_url)
    if analyze_result == "Normal":
        count += 1
        structure_test = 0
    # Validate SSL certificate for the URL
    if validate_certificate(scanned_url):
        count += 1
        certificate_test = 0
    # Check website reputation using VirusTotal API
    reputation, total_scanners = check_website_reputation(scanned_url)
    if reputation == 0:
        count += 1
        virus_total_test = 0
    # Validate TLD for the URL
    tld_result = validate_tld(scanned_url)
    if tld_result == "Valid TLD":
        count += 1
        tld_test = 0

    # Check if all tests passed
    if count == 5:
        status = "success"
        proceed_payment(logged_in_username, scanned_url)
    else:
        print("Your QR code may be suspicious. Proceed with caution.")

    # Update the database table 'test_table' with test results
    update_test_table(logged_in_username, scanned_url, url_test, certificate_test, structure_test, tld_test, virus_total_test, status)

    response_data = {
        'url_test': url_test,
        'certificate_test': certificate_test,
        'structure_test': structure_test,
        'tld_test': tld_test,
        'virus_total_test': virus_total_test,
        'status': status
    }

    return jsonify(response_data), 200

# Function to update the 'test_table' in the database
@app.route('/update_test_table', methods=['POST'])
def update_test_table_endpoint():
    request_data = request.get_json()
    username = request_data['username']
    url = request_data['url']
    url_test = request_data['url_test']
    certificate_test = request_data['certificate_test']
    structure_test = request_data['structure_test']
    tld_test = request_data['tld_test']
    virus_total_test = request_data['virus_total_test']
    status = request_data['status']

    try:
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

        return jsonify({'message': 'Test table updated successfully.'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {e}'}), 500
    finally:
        db.close()

# Function to scan QR code and save URL to scanned_url.txt
@app.route('/scan_qr_code', methods=['GET'])
def scan_qr_code_endpoint():
    def generate_frames():
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
                yield f"Scanned URL: {url}\n"
                break

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Function to test URL for maliciousness
@app.route('/test_url', methods=['POST'])
def test_url_endpoint():
    request_data = request.get_json()
    url = request_data['url']

    try:
        # Preprocess the URL
        url = preprocess(url)

        # Load the trained model from the "url.joblib" file
        model_filename = r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem5\prj\securecoding\cds\url.joblib"
        loaded_model = joblib.load(model_filename)

        # Predict the label for the URL using the loaded model
        label = loaded_model.predict([url])[0]

        # Output the result and label
        result = "False Positive" if label == 0 else "True Positive"
        response_data = {
            'classification_result': result,
            'predicted_label': label
        }

        # Check if it's a non-malicious result and update the count
        if label == "benign":
            response_data['is_malicious'] = False
        else:
            response_data['is_malicious'] = True

        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'message': f'Error: {e}'}), 500

@app.route('/analyze_url_structure', methods=['POST'])
def analyze_url_structure_endpoint():
    request_data = request.get_json()
    url = request_data['url']

    try:
        parsed_url = urllib.parse.urlparse(url)
        
        # Check for anomalies in the URL structure
        if len(parsed_url.netloc) > 50:
            result = "Suspicious"  # Long domain or subdomain
        else:
            result = "Normal"  # No anomalies detected

        response_data = {'url_structure_result': result}
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'message': f'Error: {e}'}), 500

# Function to validate SSL certificate for a given URL
@app.route('/validate_certificate', methods=['POST'])
def validate_certificate_endpoint():
    request_data = request.get_json()
    url = request_data['url']

    try:
        # Send a GET request to the URL with certifi's CA bundle
        response = requests.get(url, timeout=5, verify=certifi.where())

        if response.status_code == 200:
            result = "Certificate is valid and trusted"
        else:
            result = "Failed to retrieve the URL. May not be allowed for payment"

        response_data = {'certificate_validation_result': result}
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'message': f'Error: {e}'}), 500

# Function to check website reputation using VirusTotal API
@app.route('/check_website_reputation', methods=['POST'])
def check_website_reputation_endpoint():
    request_data = request.get_json()
    url = request_data['url']
    
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

        if scan_result.get('response_code') == 1:
            scan_id = scan_result.get('scan_id')
            
            # Retrieve the scan report
            params = {'apikey': api_key, 'resource': scan_id}
            report_response = requests.get(report_url, params=params)
            report_data = report_response.json()
            
            # Extract the reputation score and scan results
            reputation = report_data.get('positives', 0)
            total_scanners = report_data.get('total', 0)

            result = {
                'reputation_score': f'{reputation}/{total_scanners}',
                'scan_results': report_data
            }
            return jsonify(result), 200
        else:
            return jsonify({'message': 'URL scan failed. Check the URL or try again later.'}), 500
    except Exception as e:
        return jsonify({'message': f'Error: {e}'}), 500

# Function to validate TLD (Top-Level Domain)
@app.route('/validate_tld', methods=['POST'])
def validate_tld_endpoint():
    request_data = request.get_json()
    url = request_data['url']
    
    try:
        extracted = tldextract.extract(url)
        tld = extracted.suffix

        # List of trusted TLDs (add more if needed)
        trusted_tlds = ["com", "org", "net", "edu"]

        if tld in trusted_tlds:
            result = {'tld_validation_result': 'Valid TLD'}
        else:
            result = {'tld_validation_result': 'Suspicious TLD'}
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': f'Error: {e}'}), 500

# Function for URL preprocessing
@app.route('/preprocess_url', methods=['POST'])
def preprocess_url_endpoint():
    request_data = request.get_json()
    url = request_data['url']
    
    try:
        # Parse the URL
        url = urllib.parse.unquote(url)
        url = url.lower()
        # Remove http and www
        url = re.sub(r'^https?://(?:www\.)?', '', url)
        # Remove trailing slash
        url = re.sub(r'/$', '', url)

        result = {'preprocessed_url': url}
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': f'Error: {e}'}), 500


# Function for Paywave functionality
@app.route('/paywave', methods=['GET'])
def paywave_endpoint():
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
            return balance()
        elif user_choice == "2":
            return scan_qr()
        elif user_choice == "3":
            return deposit_money_endpoint()
        elif user_choice == "4":
            return transaction_history()
        elif user_choice == "5":
            logged_in_username = None  # Clear the logged-in username
            return jsonify({'message': 'Logged out successfully'}), 200
        else:
            return jsonify({'message': 'Invalid choice. Please select a valid option.'}), 400

# Function to display transaction history
@app.route('/transaction_history', methods=['GET'])
def transaction_history_endpoint():
    global logged_in_username  # Access the logged-in username
    
    try:
        db = connect_to_database()
        cursor = db.cursor()
        query = "SELECT * FROM history WHERE user_id = (SELECT user_id FROM user WHERE username = %s) ORDER BY transaction_id DESC"
        cursor.execute(query, (logged_in_username,))
        transactions = cursor.fetchall()

        if transactions:
            transaction_history_data = []
            for transaction in transactions:
                transaction_data = {
                    "Transaction ID": transaction[0],
                    "Timestamp": transaction[1].strftime('%Y-%m-%d %H:%M:%S'),
                    "URL": transaction[2],
                    "Amount": transaction[3],
                    "Status": transaction[4],
                    "Balance": transaction[6]
                }
                transaction_history_data.append(transaction_data)

            return jsonify({"Transaction History": transaction_history_data}), 200
        else:
            return jsonify({"message": "No transaction history available"}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve transaction history: {e}"}), 500
    finally:
        db.close()

@app.route('/deposit_money', methods=['POST'])
def deposit_money_endpoint():
    global logged_in_username  # Access the logged-in username
    
    try:
        request_data = request.get_json()
        deposit_amount = float(request_data['deposit_amount'])
        
        if deposit_amount <= 0:
            return jsonify({'message': 'Invalid amount. Please enter a positive amount to deposit.'}), 400

        db = connect_to_database()
        cursor = db.cursor()
        
        # Update the user's balance in the database
        query = "UPDATE user SET balance = balance + %s WHERE username = %s"
        cursor.execute(query, (deposit_amount, logged_in_username))
        db.commit()
        
        # Fetch the updated balance
        query = "SELECT balance FROM user WHERE username = %s"
        cursor.execute(query, (logged_in_username,))
        updated_balance = cursor.fetchone()[0]
        
        db.close()
        
        return jsonify({'message': f'Deposit of ${deposit_amount:.2f} successful. Your new balance is: ${updated_balance:.2f}'}), 200

    except ValueError:
        return jsonify({'message': 'Invalid input. Please enter a valid amount.'}), 400
    except Exception as e:
        return jsonify({'message': f'Failed to deposit money: {e}'}), 500
# Function to proceed with payment
@app.route('/proceed_payment', methods=['POST'])
def proceed_payment_endpoint():
    global logged_in_username  # Access the logged-in username

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

            # Parse the payment amount from the request data
            payment_amount = float(request.json.get('payment_amount'))

            # Check if the user has sufficient balance for the payment
            if payment_amount <= 0:
                return jsonify({"message": "Invalid amount. Please enter a positive amount to pay."}), 400
            elif payment_amount > current_balance:
                return jsonify({"message": "Payment failed. Insufficient balance."}), 400
            else:
                # Update the user's balance after successful payment
                new_balance = current_balance - payment_amount
                update_query = "UPDATE user SET balance = %s WHERE username = %s"
                cursor.execute(update_query, (new_balance, logged_in_username))
                db.commit()

                # Store the transaction history
                store_transaction_history(user_id, request.json.get('scanned_url'), payment_amount, "success")

                return jsonify({"message": f"Payment of ${payment_amount:.2f} successful. Your new balance is: ${new_balance:.2f}"}), 200
        else:
            return jsonify({"message": "Failed to retrieve user information."}), 500

    except ValueError:
        return jsonify({"message": "Invalid input. Please enter a valid payment amount."}), 400
    finally:
        db.close()

# Function to store transaction history
@app.route('/store_transaction_history', methods=['POST'])
def store_transaction_history_endpoint():
    try:
        db = connect_to_database()
        cursor = db.cursor()

        # Parse data from the request
        user_id = request.json.get('user_id')
        scanned_url = request.json.get('scanned_url')
        amount = request.json.get('amount')
        status = request.json.get('status')

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

            return jsonify({"message": "Transaction history stored successfully."}), 200
        else:
            return jsonify({"message": "Failed to retrieve the user's balance."}), 500

    except Exception as e:
        return jsonify({"message": f"Failed to store transaction history: {e}"}), 500
    finally:
        db.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
