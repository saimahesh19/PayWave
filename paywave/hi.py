import cv2
from pyzbar.pyzbar import decode
import urllib.parse
import re
import joblib
import requests

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

# Function to test URL for maliciousness and retrieve source code
def test_url():
    # Load the scanned URL from the file
    with open("scanned_url.txt", "r") as f:
        scanned_url = f.read().strip()
    url1 = scanned_url 
    # Preprocess the scanned URL
    url = preprocess(scanned_url)

    # Load the trained model for URL classification
    model_filename = r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem5\prj\securecoding\cds\url.joblib"
    loaded_model = joblib.load(model_filename)

    # Predict the label for the scanned URL using the loaded model
    label = loaded_model.predict([url])[0]

    # Output the result and label
    result = "Benign" if label == 0 else "Malicious"
    # print(f"The classification result is: {result}")
    print(f"The predicted label is: {label}")


# Function to preprocess URL
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
    scanned_url = scan_qr_code()
    test_url()