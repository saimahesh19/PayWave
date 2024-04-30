import tldextract

def validate_tld(url):
    extracted = tldextract.extract(url)
    tld = extracted.suffix
    
    # List of trusted TLDs (add more if needed)
    trusted_tlds = ["com", "org", "net", "edu"]
    
    if tld in trusted_tlds:
        return "Valid TLD"
    else:
        return "Suspicious TLD"

url = "https://www.phishtank.com/register.php"
result = validate_tld(url)
print(f"TLD Validation: {result}")
