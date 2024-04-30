import requests

def get_website_code():
    url = input("Enter the URL: ")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return f"Error: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Example usage
website_code = get_website_code()
print(website_code)
