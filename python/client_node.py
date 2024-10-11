import tensorflow as tf

class ClientNode:
    def __init__(self, id, w3):
        self.id = id
        self.w3 = w3
        self.address = w3.eth.accounts[id]
        self.model = self.create_model()

    def create_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(10, activation='relu', input_shape=(784,)),
            tf.keras.layers.Dense(10, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return model

    def train_local_model(self):
        # Simulate local training (replace with actual training on local data)
        self.model.fit(tf.random.normal((100, 784)), tf.random.uniform((100,), maxval=10, dtype=tf.int32), epochs=1)
        return self.model.get_weights()