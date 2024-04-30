import subprocess

# Ask the user for input (phone number)
phone_number = input("Enter the phone number: ")

# Construct the command to execute
command = f"truecallerpy -s {phone_number}"

try:
    # Execute the command
    subprocess.run(command, shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Command failed with error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

# import subprocess
# import json

# # Ask the user for input (phone number)
# phone_number = input("Enter the phone number: ")

# # Construct the command to execute
# command = f"truecallerpy -s {phone_number}"

# try:
#     # Execute the command and capture its output as a JSON string
#     result = subprocess.check_output(command, shell=True, text=True)
    
#     # Parse the JSON data
#     data = json.loads(result)
    
#     # Check if there is data available
#     if 'data' in data and 'data' in data['data'] and len(data['data']['data']) > 0:
#         info = data['data']['data'][0]
#         if 'internetAddresses' in info and len(info['internetAddresses']) > 0:
#             email_id = info['internetAddresses'][0]['id']
#             caption = info['internetAddresses'][0]['caption']
#         else:
#             email_id = "Email not found"
#             caption = "Caption not found"
#         if 'addresses' in info and len(info['addresses']) > 0:
#             city = info['addresses'][0]['city']
#         else:
#             city = "City not found"
        
#         # Display the extracted information
#         print(f"Email Address: {email_id}")
#         print(f"Caption: {caption}")
#         print(f"City: {city}")
#     else:
#         print("No information found for the provided phone number.")
# except subprocess.CalledProcessError as e:
#     print(f"Command failed with error: {e}")
# except Exception as e:
#     print(f"An error occurred: {e}")
