import numpy as np
import os
from ml_models.cnn_lstm import RULPredictor

def generate_synthetic_data(num_samples=200, sequence_length=50, num_features=4):
    """
    Generates dummy 3D time-series data for training.
    Shape: (samples, timesteps, features)
    """
    print("Generating synthetic sensor data...")
    # Generate random sensor readings (e.g., vibration, temp, acoustic, current)
    X_train = np.random.rand(num_samples, sequence_length, num_features)
    
    # Generate random Remaining Useful Life (RUL) values between 10 and 250 hours
    y_train = np.random.uniform(10, 250, size=(num_samples, 1))
    
    return X_train, y_train

def main():
    # 1. Define parameters to match what the API expects
    sequence_length = 50
    num_features = 4 
    
    # Ensure the target directory exists
    model_dir = os.path.join('ml_models', 'saved_models')
    os.makedirs(model_dir, exist_ok=True)
    # Changed from .h5 to .keras
    model_path = os.path.join(model_dir, 'cnn_lstm_rul.keras')

    # 2. Generate the fake data
    X_train, y_train = generate_synthetic_data(
        num_samples=500, 
        sequence_length=sequence_length, 
        num_features=num_features
    )

    # 3. Initialize the Predictor
    print("\n--- Initializing CNN-LSTM Model ---")
    predictor = RULPredictor(model_path=model_path)

    # 4. Build the architecture
    print("\n--- Building Architecture ---")
    predictor.build_model(sequence_length=sequence_length, num_features=num_features)

    # 5. Train the model (using a small number of epochs just to get the file saved quickly)
    print("\n--- Starting Training Loop ---")
    predictor.train(X_train, y_train, epochs=5, batch_size=32)

    print(f"\nSuccess! Dummy model trained and saved to: {model_path}")
    print("You can now start your FastAPI server and test the /predict-rul endpoint.")

if __name__ == "__main__":
    main()