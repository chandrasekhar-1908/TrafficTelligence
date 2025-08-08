import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import warnings
import os
warnings.filterwarnings('ignore')

# Generate synthetic traffic data
def generate_traffic_data(num_samples=300):
    print("Generating traffic data...")
    np.random.seed(42)
    
    # Create features
    data = {
        'hour': np.random.randint(0, 24, num_samples),
        'day_of_week': np.random.randint(0, 7, num_samples),
        'month': np.random.randint(1, 13, num_samples),
        'holiday': np.random.choice([0, 1], size=num_samples, p=[0.9, 0.1]),
        'temperature': np.random.normal(20, 10, num_samples),
        'weather_condition': np.random.choice(['Clear', 'Rain', 'Snow', 'Fog'], 
                                             size=num_samples, p=[0.7, 0.15, 0.05, 0.1]),
        'special_event': np.random.choice([0, 1], size=num_samples, p=[0.95, 0.05]),
        'road_work': np.random.choice([0, 1], size=num_samples, p=[0.9, 0.1])
    }
    
    df = pd.DataFrame(data)
    
    # Create traffic volume based on features
    base_traffic = 100
    
    # Rush hour patterns
    rush_hour = ((df['hour'].between(7, 9)) | (df['hour'].between(16, 19))).astype(int)
    df['traffic_volume'] = base_traffic + rush_hour * 200
    
    # Weekend effect
    weekend = (df['day_of_week'] >= 5).astype(int)
    df['traffic_volume'] -= weekend * 100
    
    # Holiday effect
    df['traffic_volume'] -= df['holiday'] * 150
    
    # Weather impact
    weather_impact = df['weather_condition'].map({
        'Clear': 0,
        'Rain': -30,
        'Snow': -60,
        'Fog': -40
    })
    df['traffic_volume'] += weather_impact
    
    # Special events and road work
    df['traffic_volume'] += df['special_event'] * 100
    df['traffic_volume'] -= df['road_work'] * 80
    
    # Add some random noise
    df['traffic_volume'] += np.random.normal(0, 20, num_samples)
    
    # Ensure non-negative traffic volume
    df['traffic_volume'] = df['traffic_volume'].clip(lower=0)
    
    # Convert categorical variables to one-hot encoding
    df = pd.get_dummies(df, columns=['weather_condition'])
    
    print(f"Generated data with shape: {df.shape}")
    return df

# Train and save the model
def train_model():
    try:
        print("Training model...")
        df = generate_traffic_data()
        
        # Define features and target
        features = [col for col in df.columns if col not in ['traffic_volume']]
        X = df[features]
        y = df['traffic_volume']
        
        print(f"Features: {features}")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        model = RandomForestRegressor(n_estimators=30, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        print(f"Model trained with MAE: {mae:.2f}")
        
        # Save model
        joblib.dump(model, 'traffic_model.pkl')
        joblib.dump(features, 'model_features.pkl')
        print("Model saved successfully")
        
        # Create feature importance visualization
        try:
            plt.figure(figsize=(10, 6))
            importance = model.feature_importances_
            indices = np.argsort(importance)
            plt.title('Feature Importance')
            plt.barh(range(len(indices)), importance[indices], align='center')
            plt.yticks(range(len(indices)), [features[i] for i in indices])
            plt.xlabel('Relative Importance')
            plt.tight_layout()
            
            # Create img directory if it doesn't exist
            os.makedirs('static/img', exist_ok=True)
            
            plt.savefig('static/img/feature_importance.png')
            plt.close()
            print("Feature importance image created")
        except Exception as e:
            print(f"Error creating feature importance plot: {e}")
        
        return model, features
    except Exception as e:
        print(f"Error training model: {e}")
        return None, None

# Load trained model
def load_model():
    try:
        model = joblib.load('traffic_model.pkl')
        features = joblib.load('model_features.pkl')
        print("Model loaded successfully")
        return model, features
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Training new model...")
        return train_model()

# Predict traffic volume
def predict_traffic(model, features, input_data):
    try:
        print(f"Making prediction with input: {input_data}")
        
        # Convert input to DataFrame
        input_df = pd.DataFrame([input_data])
        
        # One-hot encode weather condition
        input_df = pd.get_dummies(input_df, columns=['weather_condition'])
        
        # Ensure all required features are present
        for feature in features:
            if feature not in input_df.columns:
                input_df[feature] = 0
        
        # Reorder columns to match training data
        input_df = input_df[features]
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        print(f"Prediction result: {prediction}")
        return prediction
    except Exception as e:
        print(f"Error making prediction: {e}")
        return 100  # Return default value on error

# Test function
def test_model():
    print("Testing model...")
    model, features = load_model()
    
    if model is None or features is None:
        print("ERROR: Model or features not loaded correctly!")
        return False
    
    # Test prediction
    test_input = {
        'hour': 8,
        'day_of_week': 1,
        'month': 4,
        'holiday': 0,
        'temperature': 23,
        'weather_condition': 'Clear',
        'special_event': 0,
        'road_work': 0
    }
    
    prediction = predict_traffic(model, features, test_input)
    print(f"Test prediction: {prediction}")
    return True

if __name__ == "__main__":
    # Train the model
    model, features = train_model()
    
    # Test the model
    if model is not None and features is not None:
        test_input = {
            'hour': 8,
            'day_of_week': 1,
            'month': 4,
            'holiday': 0,
            'temperature': 23,
            'weather_condition': 'Clear',
            'special_event': 0,
            'road_work': 0
        }
        
        prediction = predict_traffic(model, features, test_input)
        print(f"Test prediction: {prediction}")
    else:
        print("Model training failed")