import os
import h5py
import numpy as np
from sklearn.model_selection import train_test_split
from cnn_lstm import RULPredictor

# Data Constants
DATA_DIR = "../../CNC_Machining-main/data"
SEQUENCE_LENGTH = 50
NUM_FEATURES = 4  # e.g., accel_x, accel_y, accel_z, temp

print("Initializing Training Pipeline")

def parse_h5_file(filepath):
    """
    Parses a single .h5 file and extracts sequence arrays.
    Returns array of shape (samples, SEQUENCE_LENGTH, NUM_FEATURES)
    """
    sequences = []
    try:
        with h5py.File(filepath, 'r') as f:
            # We assume time-series data is stored directly at the root level or in 'data'
            keys = list(f.keys())
            if len(keys) == 0:
                return []
            
            # Simple assumption: first dataset has our numeric data
            primary_dataset = f[keys[0]][:]
            
            # Trim and reshape into (samples, sequence_length, features)
            # This is a generic reshaping mechanism
            if len(primary_dataset) >= SEQUENCE_LENGTH:
                num_samples = len(primary_dataset) // SEQUENCE_LENGTH
                truncated = primary_dataset[:num_samples * SEQUENCE_LENGTH]
                
                # Reshape depending on if it has 1D or 2D shape already
                if len(truncated.shape) == 1:
                    # Pad out to NUM_FEATURES if it's purely 1D list
                    reshaped = truncated.reshape((num_samples, SEQUENCE_LENGTH))
                    full_shape = np.zeros((num_samples, SEQUENCE_LENGTH, NUM_FEATURES))
                    full_shape[:, :, 0] = reshaped
                else:
                    # e.g., shape (total_length, features)
                    feat_count = truncated.shape[1]
                    reshaped = truncated.reshape((num_samples, SEQUENCE_LENGTH, feat_count))
                    
                    full_shape = np.zeros((num_samples, SEQUENCE_LENGTH, NUM_FEATURES))
                    # Map to available features
                    copy_feats = min(feat_count, NUM_FEATURES)
                    full_shape[:, :, :copy_feats] = reshaped[:, :, :copy_feats]
                    
                sequences.append(full_shape)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

    if len(sequences) > 0:
        return np.vstack(sequences)
    return np.array([])


def load_dataset(max_samples=20000):
    """
    Finds 'good' and 'bad' states to train an Anomaly/Wear predictor.
    Limits the number of samples to prevent Out-of-Memory errors.
    """
    X_data = []
    Y_data = []

    # Map labels: 0 for good, 1 for bad (wear/anomaly)
    label_mapping = {'good': 0, 'bad': 1}
    current_samples = 0

    for machine_dir in sorted(os.listdir(DATA_DIR)):
        if current_samples >= max_samples:
            break
            
        m_path = os.path.join(DATA_DIR, machine_dir)
        if not os.path.isdir(m_path): continue

        for op_dir in sorted(os.listdir(m_path)):
            if current_samples >= max_samples:
                break
                
            op_path = os.path.join(m_path, op_dir)
            if not os.path.isdir(op_path): continue
            
            for state_label, numeric_val in label_mapping.items():
                if current_samples >= max_samples:
                    break
                    
                state_path = os.path.join(op_path, state_label)
                if not os.path.exists(state_path) or not os.path.isdir(state_path):
                    continue

                for file in os.listdir(state_path):
                    if current_samples >= max_samples:
                        print(f"Reached max sample limit ({max_samples}). Stopping load.")
                        break
                        
                    if file.endswith(".h5"):
                        file_path = os.path.join(state_path, file)
                        sequences = parse_h5_file(file_path)
                        
                        if len(sequences) > 0:
                            # If adding these sequences exceeds max_samples, truncate them
                            if current_samples + len(sequences) > max_samples:
                                allowed = max_samples - current_samples
                                sequences = sequences[:allowed]
                            
                            X_data.append(sequences)
                            Y_data.extend([numeric_val] * len(sequences))
                            current_samples += len(sequences)
    
    if len(X_data) > 0:
        return np.vstack(X_data), np.array(Y_data)
    return np.array([]), np.array([])

def main():
    print("Loading data from .h5 files...")
    X, y = load_dataset()
    
    if len(X) == 0:
        print("\nCould not extract valid structures from H5, generating mock data to ensure code functions.")
        # Fallback to verify architecture code
        X = np.random.rand(100, SEQUENCE_LENGTH, NUM_FEATURES)
        y = np.random.randint(0, 2, size=(100,))
        
    print(f"Dataset shape: {X.shape}")
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize Predictor
    model_dir = os.path.join('saved_models')
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'cnn_lstm_rul.keras')
    
    print("\n--- Initializing Model ---")
    predictor = RULPredictor(model_path=model_path)
    predictor.build_model(sequence_length=SEQUENCE_LENGTH, num_features=NUM_FEATURES)

    print("\n--- Starting Training ---")
    predictor.train(X_train, y_train, epochs=5, batch_size=32)

    print(f"\nModel saved successfully at {model_path}.")

if __name__ == "__main__":
    main()
