import requests

# Replace 'YOUR_API_KEY' with your actual VirusTotal API key
api_key = '42a1ce328eacf3efacc042b8c2fb170d944a4662fb2ea7fca75f08164e023ae9'

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
            for scanner, result in report_data.get('scans', {}).items():
                print(f'{scanner}: {result["result"]}')
        else:
            print('URL scan failed. Check the URL or try again later.')

    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    url = input("Enter a URL to check reputation: ")
    check_website_reputation(url)
