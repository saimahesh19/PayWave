# import cv2
# from pyzbar.pyzbar import decode
# import pandas as pd
# import numpy as np
# import urllib.parse
# import re
# from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
# from sklearn.pipeline import Pipeline
# import joblib

# # Function to scan QR code and save URL to scanned_url.txt
# def scan_qr_code():
#     cap = cv2.VideoCapture(0)  # Use the default camera (index 0) or specify the camera device
    
#     while True:
#         _, frame = cap.read()
#         qr_codes = decode(frame)
        
#         if qr_codes:
#             qr_code = qr_codes[0]
#             url = qr_code.data.decode('utf-8')
#             print("Scanned URL:", url)
#             with open("scanned_url.txt", "w") as f:
#                 f.write(url)
#             cap.release()
#             cv2.destroyAllWindows()
#             return url
        
#         cv2.imshow("QR Code Scanner", frame)
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# # Function to test URL for maliciousness
# def test_url():
#     # Load the scanned URL from the file
#     with open("scanned_url.txt", "r") as f:
#         scanned_url = f.read().strip()

#     # Preprocess the scanned URL
#     url = preprocess(scanned_url)

#     # Load the trained model from the "url.joblib" file
#     model_filename = r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem5\prj\securecoding\cds\url.joblib"
#     loaded_model = joblib.load(model_filename)

#     # Predict the label for the scanned URL using the loaded model
#     label = loaded_model.predict([url])[0]

#     # Output the result and label
#     result = "False Positive" if label == 0 else "True Positive"
#     print(f"The classification result is: {result}")
#     print(f"The predicted label is: {label}")

# # Function to analyze URL structure
# def analyze_url_structure(url):
#     parsed_url = urllib.parse.urlparse(url)
    
#     # Check for anomalies in the URL structure
#     if len(parsed_url.netloc) > 50:
#         return "Suspicious"  # Long domain or subdomain
    
#     return "Normal"  # No anomalies detected

# # Preprocessing function
# def preprocess(url):
#     # Parse the URL
#     url = urllib.parse.unquote(url)
#     url = url.lower()
#     # Remove http and www
#     url = re.sub(r'^https?://(?:www\.)?', '', url)
#     # Remove trailing slash
#     url = re.sub(r'/$', '', url)
#     return url

# if __name__ == "__main__":
#     scanned_url = scan_qr_code()
#     test_url()
#     analyze_result = analyze_url_structure(scanned_url)
#     print(f"URL Structure Analysis: {analyze_result}")
# ________________________________________________________________________
# import cv2
# from pyzbar.pyzbar import decode
# import pandas as pd
# import numpy as np
# import urllib.parse
# import re
# from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
# from sklearn.pipeline import Pipeline
# import joblib
# import requests
# # +_______________________________________web site repudation_______________________________________________
# # Replace 'YOUR_API_KEY' with your actual VirusTotal API key
# api_key = '42a1ce328eacf3efacc042b8c2fb170d944a4662fb2ea7fca75f08164e023ae9'

# def check_website_reputation(url):
#     try:
#         # VirusTotal API endpoint for URL scanning
#         url_scan_url = f'https://www.virustotal.com/vtapi/v2/url/scan'
        
#         # VirusTotal API endpoint for retrieving scan reports
#         report_url = f'https://www.virustotal.com/vtapi/v2/url/report'

#         # Parameters for URL scanning
#         params = {'apikey': api_key, 'url': url}
        
#         # Submit the URL for scanning
#         response = requests.post(url_scan_url, data=params)
#         scan_result = response.json()

#         # Check if the URL scan was successful
#         if scan_result.get('response_code') == 1:
#             scan_id = scan_result.get('scan_id')
            
#             # Retrieve the scan report
#             params = {'apikey': api_key, 'resource': scan_id}
#             report_response = requests.get(report_url, params=params)
#             report_data = report_response.json()
            
#             # Extract the reputation score and scan results
#             reputation = report_data.get('positives', 0)
#             total_scanners = report_data.get('total', 0)

#             # Display the results
#             print(f'Reputation Score: {reputation}/{total_scanners}')
#             print('Scan Results:')
#             for scanner, result in report_data.get('scans', {}).items():
#                 print(f'{scanner}: {result["result"]}')

#             # Check if the reputation score is greater than 0
#             if reputation > 0:
#                 print('Dangerous URL Detected!')
#             else:
#                 print('No malicious activity detected.')

#         else:
#             print('URL scan failed. Check the URL or try again later.')

#     except Exception as e:
#         print(f'Error: {e}')
# # ______________________________________________Qr scan _____________________________________________________
# # Function to scan QR code and save URL to scanned_url.txt
# def scan_qr_code():
#     cap = cv2.VideoCapture(0)  # Use the default camera (index 0) or specify the camera device
    
#     while True:
#         _, frame = cap.read()
#         qr_codes = decode(frame)
        
#         if qr_codes:
#             qr_code = qr_codes[0]
#             url = qr_code.data.decode('utf-8')
#             print("Scanned URL:", url)
#             with open("scanned_url.txt", "w") as f:
#                 f.write(url)
#             cap.release()
#             cv2.destroyAllWindows()
#             return url
        
#         cv2.imshow("QR Code Scanner", frame)
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()
# # _____________________________________________________________url test ____________________________________________
# # Function to test URL for maliciousness
# def test_url():
#     # Load the scanned URL from the file
#     with open("scanned_url.txt", "r") as f:
#         scanned_url = f.read().strip()

#     # Preprocess the scanned URL
#     url = preprocess(scanned_url)

#     # Load the trained model from the "url.joblib" file
#     model_filename = r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem5\prj\securecoding\cds\url.joblib"
#     loaded_model = joblib.load(model_filename)

#     # Predict the label for the scanned URL using the loaded model
#     label = loaded_model.predict([url])[0]

#     # Output the result and label
#     result = "False Positive" if label == 0 else "True Positive"
#     print(f"The classification result is: {result}")
#     print(f"The predicted label is: {label}")
# # ______________________________________________________structure analysis___________________________________________
# # Function to analyze URL structure
# def analyze_url_structure(url):
#     parsed_url = urllib.parse.urlparse(url)
    
#     # Check for anomalies in the URL structure
#     if len(parsed_url.netloc) > 50:
#         return "Suspicious"  # Long domain or subdomain
    
#     return "Normal"  # No anomalies detected

# # Preprocessing function
# def preprocess(url):
#     # Parse the URL
#     url = urllib.parse.unquote(url)
#     url = url.lower()
#     # Remove http and www
#     url = re.sub(r'^https?://(?:www\.)?', '', url)
#     # Remove trailing slash
#     url = re.sub(r'/$', '', url)
#     return url

# if __name__ == "__main__":
#     scanned_url = scan_qr_code()
#     test_url()
#     analyze_result = analyze_url_structure(scanned_url)
#     print(f"URL Structure Analysis: {analyze_result}")

#     # Check website reputation using VirusTotal API
#     check_website_reputation(scanned_url)

#________________________________________________________________________________________________________________

# import cv2
# from pyzbar.pyzbar import decode
# import pandas as pd
# import numpy as np
# import urllib.parse
# import re
# from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
# from sklearn.pipeline import Pipeline
# import joblib
# import requests
# import certifi

# # Replace 'YOUR_API_KEY' with your actual VirusTotal API key
# api_key = '42a1ce328eacf3efacc042b8c2fb170d944a4662fb2ea7fca75f08164e023ae9'

# # Function to scan QR code and save URL to scanned_url.txt
# def scan_qr_code():
#     cap = cv2.VideoCapture(0)  # Use the default camera (index 0) or specify the camera device
    
#     while True:
#         _, frame = cap.read()
#         qr_codes = decode(frame)
        
#         if qr_codes:
#             qr_code = qr_codes[0]
#             url = qr_code.data.decode('utf-8')
#             print("Scanned URL:", url)
#             with open("scanned_url.txt", "w") as f:
#                 f.write(url)
#             cap.release()
#             cv2.destroyAllWindows()
#             return url
        
#         cv2.imshow("QR Code Scanner", frame)
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# # Function to test URL for maliciousness
# def test_url(url):
#     # Preprocess the URL
#     url = preprocess(url)

#     # Load the trained model from the "url.joblib" file
#     model_filename = r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem5\prj\securecoding\cds\url.joblib"
#     loaded_model = joblib.load(model_filename)

#     # Predict the label for the URL using the loaded model
#     label = loaded_model.predict([url])[0]

#     # Output the result and label
#     result = "False Positive" if label == 0 else "True Positive"
#     print(f"The classification result is: {result}")
#     print(f"The predicted label is: {label}")

# # Function to analyze URL structure
# def analyze_url_structure(url):
#     parsed_url = urllib.parse.urlparse(url)
    
#     # Check for anomalies in the URL structure
#     if len(parsed_url.netloc) > 50:
#         return "Suspicious"  # Long domain or subdomain
    
#     return "Normal"  # No anomalies detected

# # Function to validate SSL certificate for a given URL
# def validate_certificate(url):
#     try:
#         # Send a GET request to the URL with certifi's CA bundle
#         response = requests.get(url, timeout=5, verify=certifi.where())
        
#         # Check if the response has a valid SSL certificate
#         if response.status_code == 200:
#             print(f"Certificate for {url} is valid and trusted.")
#         else:
#             print(f"Failed to retrieve the URL. may not allowed for payment ")
    
#     except requests.exceptions.RequestException as e:
#         print("Failed to retrieve the URL. may not allowed for payment")

# # Function to check website reputation using VirusTotal API
# def check_website_reputation(url):
#     try:
#         # VirusTotal API endpoint for URL scanning
#         url_scan_url = f'https://www.virustotal.com/vtapi/v2/url/scan'
        
#         # VirusTotal API endpoint for retrieving scan reports
#         report_url = f'https://www.virustotal.com/vtapi/v2/url/report'

#         # Parameters for URL scanning
#         params = {'apikey': api_key, 'url': url}
        
#         # Submit the URL for scanning
#         response = requests.post(url_scan_url, data=params)
#         scan_result = response.json()

#         # Check if the URL scan was successful
#         if scan_result.get('response_code') == 1:
#             scan_id = scan_result.get('scan_id')
            
#             # Retrieve the scan report
#             params = {'apikey': api_key, 'resource': scan_id}
#             report_response = requests.get(report_url, params=params)
#             report_data = report_response.json()
            
#             # Extract the reputation score and scan results
#             reputation = report_data.get('positives', 0)
#             total_scanners = report_data.get('total', 0)

#             # Display the results
#             print(f'Reputation Score: {reputation}/{total_scanners}')
#             print('Scan Results:')
#             # for scanner, result in report_data.get('scans', {}).items():
#             #     print(f'{scanner}: {result["result"]}')

#             # Check if the reputation score is greater than 0
#             if reputation > 0:
#                 print('Malicious URL Detected!')
#             else:
#                 print('No malicious activity detected.')

#         else:
#             print('URL scan failed. Check the URL or try again later.')

#     except Exception as e:
#         print(f'Error: {e}')

# # Preprocessing function
# def preprocess(url):
#     # Parse the URL
#     url = urllib.parse.unquote(url)
#     url = url.lower()
#     # Remove http and www
#     url = re.sub(r'^https?://(?:www\.)?', '', url)
#     # Remove trailing slash
#     url = re.sub(r'/$', '', url)
#     return url

# if __name__ == "__main__":
#     # Scan QR code and save URL to scanned_url.txt
#     scanned_url = scan_qr_code()

#     # Test URL for maliciousness
#     test_url(scanned_url)

#     # Analyze URL structure
#     analyze_result = analyze_url_structure(scanned_url)
#     print(f"URL Structure Analysis: {analyze_result}")

#     # Validate SSL certificate for the URL
#     validate_certificate(scanned_url)

#     # Check website reputation using VirusTotal API
#     check_website_reputation(scanned_url)
# ______________________________________________________________________________________________________________________________

import cv2
from pyzbar.pyzbar import decode
import pandas as pd
import numpy as np
import urllib.parse
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
import joblib
import requests
import certifi
import tldextract

# Replace 'YOUR_API_KEY' with your actual VirusTotal API key
api_key = '42a1ce328eacf3efacc042b8c2fb170d944a4662fb2ea7fca75f08164e023ae9'

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
# ___________________1.url test_______________________________________________________________________________________________
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

# ___________________2.URL structure test_______________________________________________________________________________________________
# Function to analyze URL structure
def analyze_url_structure(url):
    parsed_url = urllib.parse.urlparse(url)
    
    # Check for anomalies in the URL structure
    if len(parsed_url.netloc) > 50:
        return "Suspicious"  # Long domain or subdomain
    
    return "Normal"  # No anomalies detected

# ___________________3.SSL certificate test___________________________________________________________________________________________
# Function to validate SSL certificate for a given URL
def validate_certificate(url):
    try:
        # Send a GET request to the URL with certifi's CA bundle
        response = requests.get(url, timeout=5, verify=certifi.where())
        
        # Check if the response has a valid SSL certificate
        if response.status_code == 200:
            print(f"Certificate for {url} is valid and trusted.")
        else:
            print(f"Failed to retrieve the URL. may not allowed for payment ")
    
    except requests.exceptions.RequestException as e:
        print("Failed to retrieve the URL. may not allowed for payment")

# ___________________4.website reputation test__________________________________________________________________________________________
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
            # for scanner, result in report_data.get('scans', {}).items():
            #     print(f'{scanner}: {result["result"]}')

            # Check if the reputation score is greater than 0
            if reputation > 0:
                print('Malicious URL Detected!')
            else:
                print('No malicious activity detected.')

        else:
            print('URL scan failed. Check the URL or try again later.')

    except Exception as e:
        print(f'Error: {e}')

# ______________________________5. TLD  ________________________________________________________________________________________________
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

if __name__ == "__main__":
    # Scan QR code and save URL to scanned_url.txt
    scanned_url = scan_qr_code()

    # Test URL for maliciousness
    test_url(scanned_url)

    # Analyze URL structure
    analyze_result = analyze_url_structure(scanned_url)
    print(f"URL Structure Analysis: {analyze_result}")

    # Validate SSL certificate for the URL
    validate_certificate(scanned_url)

    # Check website reputation using VirusTotal API
    check_website_reputation(scanned_url)

    # Validate TLD for the URL
    tld_result = validate_tld(scanned_url)
    print(f"TLD Validation: {tld_result}")
