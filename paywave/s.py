import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from joblib import dump

# Load your dataset (replace 'dataset.csv' with your actual file)
data = pd.read_csv(r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem5\prj\securecoding\urldata.csv")

# Split the data into features (URLs) and labels
urls = data['url']
labels = data['label']

# Convert URLs to numerical features using CountVectorizer
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(urls)
y = labels.values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define a simple neural network model
model = Sequential([
    Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Define a data generator
def data_generator(X, y, batch_size):
    num_samples = X.shape[0]
    num_batches = num_samples // batch_size
    
    while True:
        indices = np.arange(num_samples)
        np.random.shuffle(indices)
        for i in range(num_batches):
            batch_indices = indices[i * batch_size: (i + 1) * batch_size]
            yield X[batch_indices], y[batch_indices]

batch_size = 32

# Train the model using the generator
model.fit(data_generator(X_train, y_train, batch_size), steps_per_epoch=X_train.shape[0] // batch_size, epochs=10, validation_split=0.1)

# Evaluate the model on the test set
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {accuracy:.2f}")

# Save the trained model
model.save('malicious_url_model')

# Save the vectorizer using joblib
dump(vectorizer, 'vectorizer.joblib')
 