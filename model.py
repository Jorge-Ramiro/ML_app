import tensorflow as tf 
from keras.models import load_model


class Model:
    def __init__(self) -> None:
        self.model = load_model("Weights/classifier_weights.h5")

    def predict(self, img_array):
        img_array = tf.convert_to_tensor(img_array)
        pred = self.model.predict(img_array)
        # aquí sigue el codigo para decir el nombre de la raza
        if pred > .5:
            print("Es un perro")
            yield "Perro"
        else:
            print("Es un gato")
            yield "Gato"

