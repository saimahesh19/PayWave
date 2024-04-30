import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import joblib

# Load the dataset
dataset = pd.read_csv(r"C:\\Users\\SAI MAHESH\\Desktop\\files\\cipher game\\XSS_dataset.csv")

# Prepare the data
X = dataset['Payload']
y = dataset['Label']

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Transform the data
X = vectorizer.fit_transform(X)

# Train the SVM classifier
svm = SVC(kernel='linear')
svm.fit(X, y)

# Save the trained model to a file
model_filename = 'trained_svm_model.pkl'
joblib.dump(svm, model_filename)

print(f"Trained SVM model saved to {model_filename}")

# Interactive interface
while True:
    # Get user input
    code_snippet = input("Enter the code snippet (or 'exit' to quit):\n")

    if code_snippet.lower() == 'exit':
        break

    # Transform the user input using the same vectorizer
    input_vector = vectorizer.transform([code_snippet])

    # Predict the label for the user input
    prediction = svm.predict(input_vector)

    # Print the prediction result
    if prediction[0] == 1:
        print("Potential XSS attack detected!")
    else:
        print("No XSS attack detected.")
