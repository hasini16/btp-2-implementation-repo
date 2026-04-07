import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv1D, MaxPooling1D, LSTM, Dense, Dropout, Flatten
import os

# Monkey-patch Dense to ignore quantization_config
_original_dense_init = Dense.__init__
def _patched_dense_init(self, *args, **kwargs):
    kwargs.pop('quantization_config', None)
    _original_dense_init(self, *args, **kwargs)
Dense.__init__ = _patched_dense_init

# Also patch keras.src.layers.core.dense.Dense directly in case of different import path
try:
    import keras.src.layers.core.dense
    keras.src.layers.core.dense.Dense.__init__ = _patched_dense_init
except ImportError:
    pass

class RULPredictor:
    def __init__(self, model_path='saved_models/cnn_lstm_rul.keras'):
       # Change this line in your __init__ method (around line 8):
        self.model_path = model_path
        self.model = None
        
        # Load the model if it already exists
        if os.path.exists(self.model_path):
            self.model = load_model(self.model_path)
            print(f"Loaded existing model from {self.model_path}")

    def build_model(self, sequence_length, num_features):
        """
        Constructs the CNN-LSTM architecture.
        - CNN layers extract spatial features from the raw sensor signals.
        - LSTM layers learn the degradation patterns over time.
        """
        self.model = Sequential()
        
        # CNN block for feature extraction
        self.model.add(Conv1D(filters=64, kernel_size=3, activation='relu', 
                              input_shape=(sequence_length, num_features)))
        self.model.add(MaxPooling1D(pool_size=2))
        self.model.add(Dropout(0.2))

        # LSTM block for sequence learning
        self.model.add(LSTM(50, return_sequences=True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(50, return_sequences=False))
        self.model.add(Dropout(0.2))

        # Fully connected block for RUL regression output
        self.model.add(Dense(32, activation='relu'))
        self.model.add(Dense(1, activation='linear')) # Linear activation for regression (RUL in hours/cycles)

        self.model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        print(self.model.summary())
        return self.model

    def train(self, X_train, y_train, epochs=50, batch_size=32, validation_split=0.2):
        """Trains the model and saves the weights."""
        if self.model is None:
            raise ValueError("Model not built. Call build_model() first.")
            
        print("Starting training...")
        history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            verbose=1
        )
        
        # Ensure the directory exists before saving
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        self.model.save(self.model_path)
        print(f"Model saved to {self.model_path}")
        return history

    def predict(self, sensor_data):
        """
        Predicts RUL from a single sequence of sensor data.
        Expected shape: (1, sequence_length, num_features)
        """
        if self.model is None:
             raise ValueError("Model not loaded or built.")
             
        prediction = self.model.predict(sensor_data)
        return float(prediction[0][0])