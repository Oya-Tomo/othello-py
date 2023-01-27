import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class Bias(keras.layers.Layer):
    def __init__(self, input_shape):
        super(Bias, self).__init__()
        self.W = tf.Variable(initial_value=tf.zeros(input_shape[1:]), trainable=True)

    def call(self, inputs):
        return inputs + self.W

model = keras.Sequential()
model.add(layers.Input(shape=(8, 8, 1)))
model.add(layers.Conv2D(1024, kernel_size=3, padding="same", activation="relu"))
model.add(layers.Conv2D(1024, kernel_size=3, padding="same", activation="relu"))
model.add(layers.Conv2D(1024, kernel_size=3, padding="same", activation="relu"))
model.add(layers.Conv2D(512, kernel_size=3, padding="same", activation="relu"))
model.add(layers.Conv2D(512, kernel_size=3, padding="same", activation="relu"))
model.add(layers.Conv2D(512, kernel_size=3, padding="same", activation="relu"))
model.add(layers.Conv2D(256, kernel_size=3, padding="same", activation="relu"))
model.add(layers.Conv2D(256, kernel_size=3, padding="same", activation="relu"))
model.add(layers.Conv2D(256, kernel_size=3, padding="same", activation="relu"))
model.add(layers.Conv2D(128, kernel_size=3, padding="same", activation="relu"))
model.add(layers.Conv2D(128, kernel_size=3, padding="same", activation="relu"))
model.add(layers.Conv2D(128, kernel_size=3, padding="same", activation="relu"))
model.add(layers.Conv2D(64, kernel_size=3, padding="same", activation="relu"))
model.add(layers.Conv2D(64, kernel_size=3, padding="same", activation="relu"))
model.add(layers.Conv2D(64, kernel_size=3, padding="same", activation="relu"))
model.add(layers.Conv2D(1, kernel_size=1, use_bias=False))
model.add(layers.Flatten())
model.add(Bias((1, 64)))
model.add(layers.Activation('softmax'))

model.compile(keras.optimizers.SGD(learning_rate=0.01, momentum=0.0, decay=0.0, nesterov=False), 'categorical_crossentropy', metrics=['accuracy'])
model.summary()

model.save("./models/model5")