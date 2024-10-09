import tensorflow as tf

class ClientNode:
    def __init__(self, id, w3):
        self.id = id
        self.w3 = w3
        self.address = w3.eth.accounts[id]
        self.model = self.create_model()
        self.dataset_size = 100  # Set a sample dataset size; replace with actual size if needed

    def create_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(10, activation='relu', input_shape=(784,)),
            tf.keras.layers.Dense(10, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return model

    def train_local_model(self):
        # Simulate local training (replace with actual training on local data)
        self.model.fit(tf.random.normal((self.dataset_size, 784)), 
                        tf.random.uniform((self.dataset_size,), maxval=10, dtype=tf.int32), 
                        epochs=1)
        return self.model.get_weights()

    def get_weight(self):
        # Here we can define the weight based on the dataset size or other criteria
        return self.dataset_size  # For now, return dataset size as weight
