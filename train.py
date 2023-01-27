import tensorflow as tf
from tensorflow import keras
import numpy as np

model_name = "models/model1"

npz_file = np.load("data/wthor-0.npz")

board_data = npz_file["arr_0"]
moves_data = npz_file["arr_1"]

model = tf.keras.models.load_model(model_name)

x_train = board_data
y_train = moves_data.reshape((-1, 64))

try:
    model.fit(x_train, y_train, epochs=3, batch_size=32, validation_split=0.2)
except KeyboardInterrupt:
    # model.save(model_name)
    pass

model.save(model_name)