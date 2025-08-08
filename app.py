from flask import Flask, render_template, request, jsonify
import os
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Import model functions
from model import load_model, predict_traffic

# Load the model
print("Loading model...")
model, features = load_model()

if model is None or features is None:
    print("ERROR: Model or features not loaded correctly!")
else:
    print("Model loaded successfully")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from form
        input_data = {
            'hour': int(request.form.get('hour', 12)),
            'day_of_week': int(request.form.get('day_of_week', 1)),
            'month': int(request.form.get('month', 6)),
            'holiday': int(request.form.get('holiday', 0)),
            'temperature': float(request.form.get('temperature', 20)),
            'weather_condition': request.form.get('weather_condition', 'Clear'),
            'special_event': int(request.form.get('special_event', 0)),
            'road_work': int(request.form.get('road_work', 0))
        }
        
        print(f"Input data: {input_data}")
        
        # Make prediction
        prediction = predict_traffic(model, features, input_data)
        
        # Determine traffic status
        if prediction < 100:
            status = "Low Traffic"
            status_color = "green"
        elif prediction < 200:
            status = "Moderate Traffic"
            status_color = "yellow"
        else:
            status = "Heavy Traffic"
            status_color = "red"
        
        result = {
            'prediction': round(prediction, 2),
            'status': status,
            'status_color': status_color
        }
        
        print(f"Returning result: {result}")
        return jsonify(result)
    except Exception as e:
        print(f"Error in prediction route: {e}")
        return jsonify({
            'prediction': 100,
            'status': "Error",
            'status_color': "gray"
        })

if __name__ == '__main__':
    # Create static/img directory if it doesn't exist
    os.makedirs('static/img', exist_ok=True)
    print("Starting Flask app...")
    app.run(debug=True)