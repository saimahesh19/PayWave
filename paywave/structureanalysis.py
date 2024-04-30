import urllib.parse

def analyze_url_structure(url):
    parsed_url = urllib.parse.urlparse(url)
    
    # Check for anomalies in the URL structure
    if len(parsed_url.netloc) > 50:
        return "Suspicious"  # Long domain or subdomain
    
    return "Normal"  # No anomalies detected

url = "https://www.phishtank.com/register.php"
result = analyze_url_structure(url)
print(f"URL Structure Analysis: {result}")