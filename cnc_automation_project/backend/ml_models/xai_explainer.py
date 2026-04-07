import numpy as np
import lime
import lime.lime_tabular

class ModelExplainer:
    def __init__(self, training_data, feature_names):
        """
        Initializes the LIME explainer.
        Note: LIME expects tabular (2D) data. Since we are using 3D time-series 
        data (samples, timesteps, features), we typically flatten the temporal 
        dimension or explain the features at the most recent timestep.
        
        For this implementation, we will explain based on a flattened snapshot.
        """
        # Flatten the 3D training data (samples, timesteps, features) to 2D for LIME
        self.num_timesteps = training_data.shape[1]
        self.num_features = training_data.shape[2]
        
        flattened_training_data = training_data.reshape(
            training_data.shape[0], 
            self.num_timesteps * self.num_features
        )

        # Generate flattened feature names (e.g., "Vibration_t-5", "Temp_t-0")
        flattened_feature_names = [
            f"{feat}_t-{self.num_timesteps - t - 1}" 
            for t in range(self.num_timesteps) 
            for feat in feature_names
        ]

        self.explainer = lime.lime_tabular.LimeTabularExplainer(
            flattened_training_data,
            feature_names=flattened_feature_names,
            class_names=['RUL'],
            mode='regression'
        )

    def explain_prediction(self, model_predict_fn, instance):
        """
        Generates an explanation for a specific prediction.
        instance: The 3D input instance (1, timesteps, features)
        """
        flattened_instance = instance.flatten()

        # Wrap the model's prediction function to handle flattened data from LIME
        def predict_wrapper(flattened_data):
            # Reshape back to 3D for the CNN-LSTM
            reshaped_data = flattened_data.reshape(
                flattened_data.shape[0], 
                self.num_timesteps, 
                self.num_features
            )
            return model_predict_fn(reshaped_data)

        # Generate the explanation
        explanation = self.explainer.explain_instance(
            flattened_instance, 
            predict_wrapper, 
            num_features=5 # Show top 5 contributing factors
        )
        
        return explanation.as_list()