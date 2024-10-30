from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import CORS
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
from cm import CM

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load your trained model (ensure the model file is in the same directory)
model = load_model('combined_inception_efficientnet_classifier.h5')

# Labels for the classification
CLASS_LABELS = ['potato_early_blight', 'potato_healthy', 'potato_late_blight',
                'corn_common_rust', 'corn_healthy', 'corn_northern_leaf_blight', 'corn_gray_leaf_spot']

# Preprocess image
# Preprocess image
def preprocess_image(image, target_size=(380, 380)):  # Change target size to (380, 380)
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    image = image / 255.0  # Normalize to [0, 1]
    return image

# Route for homepage
@app.route('/')
def home():
    return render_template('index.html')

# Map the misclassified labels to the correct ones

# Route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']
    if file:
        print(f"File uploaded: {file.filename}")
        try:
            image = Image.open(file)
            processed_image = preprocess_image(image)

            # Make prediction
            predictions = model.predict(processed_image)
            predicted_class = np.argmax(predictions, axis=1)
            result = CLASS_LABELS[predicted_class[0]]

            # Check if the result needs to be corrected
            if result in CM:
                corrected_result = CM[result]
                print(f"Original prediction: {result}, Corrected to: {corrected_result}")
                result = corrected_result  # Override the result with the corrected label

            return jsonify({'prediction': result})
        except Exception as e:
            print(f"Error during prediction: {e}")
            return jsonify({'error': 'Error processing the image'})
    else:
        return jsonify({'error': 'Something went wrong'})

# Dummy route to return 'Hello' message
@app.route('/hello', methods=['POST'])
def hello():
    return jsonify({'message': 'Hello from the backend'})  # Dummy message response

if __name__ == '__main__':
    app.run(debug=True)
