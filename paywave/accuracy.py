import pandas as pd
import numpy as np
import urllib.parse
import re
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv(r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem4\machine learning in cyber security\urldata.csv")

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

# Preprocess the URLs in the dataset
df['url'] = df['url'].apply(preprocess)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['url'], df['label'], test_size=0.2)

# Define the pipeline
pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', LogisticRegression())
])

# Train the pipeline
pipeline.fit(X_train, y_train)

# Save the trained model to a file
model_filename = "trained_model.joblib"
joblib.dump(pipeline, model_filename)

# Get user input for a URL to classify
user_input = input("Enter a URL to classify: ")
url = preprocess(user_input)

# Load the trained model from the file
loaded_model = joblib.load(model_filename)

# Predict the label for the user input URL using the loaded model
label = loaded_model.predict([url])[0]

# Output the result and label
result = "False Positive" if label == 0 else "True Positive"
print(f"The classification result is: {result}")
print(f"The predicted label is: {label}")

# Calculate accuracy on the test set
y_pred = loaded_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Generate and display the confusion matrix using seaborn
conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 4))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar=False, square=True)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()
