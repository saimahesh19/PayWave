# AIzaSyCOFJGwqrwBha3SiF4-T_G7Cz6I7in2ELo
import requests

def check_domain_reputation(url):
    api_key = 'AIzaSyCOFJGwqrwBha3SiF4-T_G7Cz6I7in2ELo'
    safe_browsing_url = f'https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}'
    
    payload = {
        "client": {
            "clientId": "your-app-name",
            "clientVersion": "1.0",
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "PHISHING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}],
        },
    }

    response = requests.post(safe_browsing_url, json=payload)
    data = response.json()
    
    if "matches" in data:
        return "Malicious (Google Safe Browsing)"  # The domain is associated with malicious activities according to Google Safe Browsing
    else:
        # Perform additional checks with PhishTank or other services here.
        phishtank_result = check_phishtank_reputation(url)
        if phishtank_result == "Phishing":
            return "Malicious (PhishTank)"  # The domain is flagged as phishing by PhishTank
        else:
            return "Safe"  # The domain is not associated with known threats

def check_phishtank_reputation(url):
    # Implement PhishTank reputation check here
    # You can use their API or database to check for phishing URLs
    # Return "Phishing" or "Safe" based on the result

    user_url = input("Enter the URL to check: ")
    result = check_domain_reputation(user_url)
    print(f"Domain Reputation: {result}")
