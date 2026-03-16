import tensorflow as tf
import numpy as np


class GradCAM:
    def __init__(self, model, layer_name):
        self.model = model
        self.layer_name = layer_name
    
    def generate_heatmap(self, img_array):
        """Generate Grad-CAM heatmap for the given image"""
        img_array = tf.cast(img_array, tf.float32)
        
        # Create a model that outputs both the target layer and the final output
        try:
            target_layer = self.model.get_layer(self.layer_name)
            grad_model = tf.keras.models.Model(
                [self.model.inputs[0] if isinstance(self.model.inputs, list) else self.model.inputs],
                [target_layer.output, self.model.output]
            )
        except Exception as e:
            # Fallback to a simpler approach if grad model creation fails
            print(f"Warning: Could not create grad model: {e}. Using fallback heatmap.")
            return self._generate_simple_heatmap(img_array)
        
        # Compute gradients
        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_array, training=False)
            # Get the class with the highest prediction
            predicted_class = tf.argmax(predictions[0])
            class_channel = predictions[:, predicted_class]
        
        # Get gradients of the class output w.r.t. the convolutional layer output
        grads = tape.gradient(class_channel, conv_outputs)
        
        if grads is None:
            print("Warning: Gradient computation failed. Using fallback heatmap.")
            return self._generate_simple_heatmap(img_array)
        
        # Pool the gradients over spatial dimensions
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        
        # Weight the convolutional outputs by the pooled gradients using broadcasting
        # Reshape pooled_grads to (1, 1, num_channels) for broadcasting with conv_outputs (height, width, num_channels)
        conv_outputs = conv_outputs[0]  # Remove batch dimension: (height, width, channels)
        pooled_grads_expanded = tf.reshape(pooled_grads, (1, 1, pooled_grads.shape[0]))  # (1, 1, channels)
        
        # Use tf.multiply for element-wise multiplication (broadcasting automatically handles spatial dims)
        weighted_conv_outputs = tf.multiply(conv_outputs, pooled_grads_expanded)
        
        # Create heatmap
        heatmap = tf.reduce_mean(weighted_conv_outputs, axis=-1)
        heatmap = tf.maximum(heatmap, 0)
        heatmap = heatmap / (tf.reduce_max(heatmap) + 1e-8)
        
        return heatmap.numpy()
    
    def _generate_simple_heatmap(self, img_array):
        """
        Fallback method to generate a simple heatmap based on channel activations.
        Gracefully handles missing layers by catching exceptions.
        """
        try:
            # Attempt to get the target layer
            target_layer = self.model.get_layer(self.layer_name)
            
            # Create a model that outputs the target layer's activations
            target_layer_model = tf.keras.models.Model(
                [self.model.inputs[0] if isinstance(self.model.inputs, list) else self.model.inputs],
                target_layer.output
            )
            activations = target_layer_model(img_array)
            
        except (ValueError, AttributeError) as e:
            # Handle missing layer by trying the last convolutional layer
            print(f"Warning: Could not find layer '{self.layer_name}': {e}")
            print("Attempting to use last convolutional layer...")
            
            last_conv_layer = None
            for layer in reversed(self.model.layers):
                if 'conv' in layer.name.lower():
                    last_conv_layer = layer
                    break
            
            if last_conv_layer is None:
                print("Error: No convolutional layer found in the model. Cannot generate heatmap.")
                return None
            
            try:
                target_layer_model = tf.keras.models.Model(
                    [self.model.inputs[0] if isinstance(self.model.inputs, list) else self.model.inputs],
                    last_conv_layer.output
                )
                activations = target_layer_model(img_array)
                print(f"Successfully using fallback layer: {last_conv_layer.name}")
            except Exception as fallback_error:
                print(f"Error: Failed to create model with fallback layer: {fallback_error}")
                return None
        
        # Average across channels to create heatmap
        heatmap = tf.reduce_mean(activations[0], axis=-1)
        heatmap = tf.maximum(heatmap, 0)
        heatmap = heatmap / (tf.reduce_max(heatmap) + 1e-8)
        
        return heatmap.numpy()
    
    def get_prediction(self, img_array):
        img_array = tf.cast(img_array, tf.float32)
        predictions = self.model.predict(img_array, verbose=0)
        return predictions[0]
