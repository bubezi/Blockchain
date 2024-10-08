import tensorflow as tf

class ClientNode:
    def __init__(self, model, dataset):
        self.model = model
        self.dataset = dataset

    def train_local_model(self, epochs=5, batch_size=32):
        self.model.fit(self.dataset, epochs=epochs, batch_size=batch_size)

    def get_model_update(self):
        return self.model.get_weights()

# Usage
model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu', input_shape=(784,)),
    tf.keras.layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

client = ClientNode(model, mnist_dataset)
client.train_local_model()
model_update = client.get_model_update()
