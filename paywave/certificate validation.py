import requests
import certifi

def validate_certificate(url):
    try:
        # Send a GET request to the URL with certifi's CA bundle
        response = requests.get(url, timeout=5, verify=certifi.where())
        
        # Check if the response has a valid SSL certificate
        if response.status_code == 200:
            print(f"Certificate for {url} is valid and trusted.")
        else:
            print(f"Failed to retrieve the URL. Status code: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print("An error occurred:", str(e))

# Get URL input from the user
url_to_check = input("Enter the URL to check the SSL certificate: ")
validate_certificate(url_to_check)
