# import pandas as pd
# import numpy as np
# import urllib.parse
# import re
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
# from sklearn.pipeline import Pipeline
# from sklearn.linear_model import LogisticRegression
# import joblib  # Import joblib for model persistence

# # Load the dataset
# df = pd.read_csv(r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem4\machine learning in cyber security\urldata.csv")

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

# # Save the trained model to a file
# model_filename = "trained_model.joblib"
# joblib.dump(pipeline, model_filename)

# # Get user input for a URL to classify
# user_input = input("Enter a URL to classify: ")
# url = preprocess(user_input)

# # Load the trained model from the file
# loaded_model = joblib.load(model_filename)

# # Predict the label for the user input URL using the loaded model
# label = loaded_model.predict([url])[0]

# # Output the result and label
# result = "False Positive" if label == 0 else "True Positive"
# print(f"The classification result is: {result}")
# print(f"The predicted label is: {label}")
# ____________________________________________________________________________________

# import pandas as pd
# import numpy as np
# import urllib.parse
# import re
# from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
# from sklearn.pipeline import Pipeline
# import joblib

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

# # Get user input for a URL to classify
# user_input = input("Enter a URL to classify: ")
# url = preprocess(user_input)

# # Load the trained model from the "url.joblib" file
# model_filename = r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem5\prj\securecoding\cds\url.joblib"
# loaded_model = joblib.load(model_filename)

# # Predict the label for the user input URL using the loaded model
# label = loaded_model.predict([url])[0]

# # Output the result and label
# result = "False Positive" if label == 0 else "True Positive"
# print(f"The classification result is: {result}")
# print(f"The predicted label is: {label}")

# ______________________________________________________________
# import pandas as pd
# import numpy as np
# import urllib.parse
# import re
# from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
# from sklearn.pipeline import Pipeline
# import joblib

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

# # Load the scanned URL from the file
# with open("scanned_url.txt", "r") as f:
#     scanned_url = f.read().strip()

# # Preprocess the scanned URL
# url = preprocess(scanned_url)

# # Load the trained model from the "url.joblib" file
# model_filename = r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem5\prj\securecoding\cds\url.joblib"
# loaded_model = joblib.load(model_filename)

# # Predict the label for the scanned URL using the loaded model
# label = loaded_model.predict([url])[0]

# # Output the result and label
# result = "False Positive" if label == 0 else "True Positive"
# print(f"The classification result is: {result}")
# print(f"The predicted label is: {label}")
import pandas as pd
import numpy as np
import urllib.parse
import re
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline

# Load the dataset
df = pd.read_csv(r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem4\machine learning in cyber security\urldata.csv")

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
X_train, X_test, y_train, y_test = train_test_split(df['url'], df['label'], test_size=0.2, random_state=42)

# Define the pipeline with an AdaBoost classifier
# Here, we use a DecisionTreeClassifier as a base estimator, but you can replace it with other classifiers
base_classifier = DecisionTreeClassifier(max_depth=1)  # You can adjust the parameters of the base classifier
adaboost_classifier = AdaBoostClassifier(base_classifier, n_estimators=50, random_state=42)  # You can adjust the number of estimators

pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer(use_idf=False)),  # Disable TF-IDF
    ('clf', adaboost_classifier)
])

# Train the pipeline
pipeline.fit(X_train, y_train)

# Calculate and display accuracy, precision, recall, and F1-score
y_pred = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, pos_label="malicious")  # Specify the positive label
recall = recall_score(y_test, y_pred, pos_label="malicious")  # Specify the positive label
f1 = f1_score(y_test, y_pred, pos_label="malicious")  # Specify the positive label

print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")
