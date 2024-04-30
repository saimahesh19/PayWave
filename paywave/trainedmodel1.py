# <!-- can we stored trained model?? if yes how can we store it 
# ChatGPT
# Yes, you can definitely store a trained machine learning model, including an SVM model, for future use without retraining. One common way to store a trained model is by using the joblib library (part of the scikit-learn ecosystem) or the built-in pickle module in Python.

# Here's how you can modify your code to save and load a trained SVM model using the joblib library: -->

import pandas as pd
import numpy as np
import urllib.parse
import re
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
import joblib

# Load the dataset
df = pd.read_csv(r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem5\prj\securecoding\urldata.csv")

# Preprocessing function
def preprocess(url):
    url = urllib.parse.unquote(url)
    url = url.lower()
    url = re.sub(r'^https?://(?:www\.)?', '', url)
    url = re.sub(r'/$', '', url)
    return url

# Preprocess the URLs in the dataset
df['url'] = df['url'].apply(preprocess)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['url'], df['label'], test_size=0.2)

# Define the pipeline
pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', SVC(kernel='linear'))
])

# Train the pipeline
pipeline.fit(X_train, y_train)

# Save the trained model to a file
model_filename = 'svm_model.joblib'
joblib.dump(pipeline, model_filename)

# Get user input for a URL to classify
user_input = input("Enter a URL to classify: ")
url = preprocess(user_input)

# Load the trained model from the file
loaded_model = joblib.load(model_filename)

# Predict the label for the user input URL using the loaded model
label = loaded_model.predict([url])[0]

# Output the result and label
result = "Malicious" if label == 1 else "Benign"
print(f"The classification result is: {result}")
print(f"The predicted label is: {label}")


# In this code, the joblib library is used to save the trained SVM model to a file named svm_model.joblib. Later, the model is loaded from the file and used for making predictions on user input URLs.