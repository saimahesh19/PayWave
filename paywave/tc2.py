import subprocess

def main():
    phone_number = input("Enter the phone number: ")
    
    # Construct the command to execute
    command = ["truecallerpy", "-s", phone_number]
    
    try:
        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Print the output
        print(result.stdout)
        
        if result.returncode != 0:
            print("An error occurred.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
