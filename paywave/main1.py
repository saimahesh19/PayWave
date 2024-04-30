import cv2
from pyzbar.pyzbar import decode
import urllib.parse
import re
import requests
import certifi
import tldextract
import joblib

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

if __name__ == "__main__":
    # Scan QR code and save URL to scanned_url.txt
    scanned_url = scan_qr_code()

    # Initialize count variable to track non-malicious test cases
    count = 0

    # Test URL for maliciousness
    if test_url(scanned_url):
        count += 1
        print("test 1 ")
    # Analyze URL structure
    analyze_result = analyze_url_structure(scanned_url)
    if analyze_result == "Normal":
        count += 1
        print("test 2")
    # Validate SSL certificate for the URL
    if validate_certificate(scanned_url):
        count += 1
        print("test 3")
    # Check website reputation using VirusTotal API
    reputation, total_scanners = check_website_reputation(scanned_url)
    if reputation == 0:
        count += 1
        print("test 4 ")
    # Validate TLD for the URL
    tld_result = validate_tld(scanned_url)
    if tld_result == "Valid TLD":
        count += 1
        print("test 5")
    print(count)
    # Check if count is 5 (all non-malicious tests passed)
    if count == 5:
        print("Your QR code is safe to use.")
    else:
        print("Your QR code may be suspicious. Proceed with caution.")
