# import cv2
# from pyzbar.pyzbar import decode
# import pandas as pd
# import numpy as np
# import urllib.parse
# import re
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
# from sklearn.pipeline import Pipeline
# from sklearn.linear_model import LogisticRegression

# # Load the dataset
# df = pd.read_csv(r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem5\prj\securecoding\urldata.csv")

# # Preprocessing function
# def preprocess(url):
#     # Parse the URL
#     url = urllib.parse.unquote(url)
#     url = url.lower()
#     # Remove http and www
#     url = re.sub(r'^https?://(?:www\.)?', '', url)
#     # Remove trailing slash
#     url = re.sub(r'/$', '', url)
#     return url

# # Preprocess the URLs in the dataset
# df['url'] = df['url'].apply(preprocess)

# # Split the dataset into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(df['url'], df['label'], test_size=0.2)

# # Define the pipeline
# pipeline = Pipeline([
#     ('vect', CountVectorizer()),
#     ('tfidf', TfidfTransformer()),
#     ('clf', LogisticRegression())
# ])

# # Train the pipeline
# pipeline.fit(X_train, y_train)

# # Function to scan QR code and classify URL
# def scan_and_classify():
#     cap = cv2.VideoCapture(0)  # Use the default camera (index 0) or specify the camera device

#     while True:
#         _, frame = cap.read()
#         qr_codes = decode(frame)

#         if qr_codes:
#             qr_code = qr_codes[0]
#             url = qr_code.data.decode('utf-8')
#             print("Scanned URL:", url)
            
#             # Preprocess the scanned URL
#             url = preprocess(url)
            
#             # Predict the label for the scanned URL
#             label = pipeline.predict([url])[0]

#             # Output the result and label
#             result = "Malicious" if label == 1 else "Not Malicious"
#             print(f"The classification result is: {result}")
#             break

#         cv2.imshow("QR Code Scanner", frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# # Example usage
# scan_and_classify()




import cv2
from pyzbar.pyzbar import decode
import pandas as pd
import numpy as np
import urllib.parse
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
import joblib

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
def test_url():
    # Load the scanned URL from the file
    with open("scanned_url.txt", "r") as f:
        scanned_url = f.read().strip()

    # Preprocess the scanned URL
    url = preprocess(scanned_url)

    # Load the trained model from the "url.joblib" file
    model_filename = r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem5\prj\securecoding\cds\url.joblib"
    loaded_model = joblib.load(model_filename)

    # Predict the label for the scanned URL using the loaded model
    label = loaded_model.predict([url])[0]

    # Output the result and label
    result = "False Positive" if label == 0 else "True Positive"
    print(f"The classification result is: {result}")
    print(f"The predicted label is: {label}")

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
    scanned_url = scan_qr_code()
    test_url()
