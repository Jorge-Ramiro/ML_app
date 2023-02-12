from tensorflow import convert_to_tensor
from keras.models import load_model
import pandas as pd


class Model:
    def __init__(self) -> None:
        self.model = load_model("Weights/classifier_weights.h5")
        self.class_names = pd.read_csv("class_names.csv")

    def predict(self, img_array):
        img_array = convert_to_tensor(img_array)
        pred = self.model.predict(img_array)
        # aquí sigue el codigo para decir el nombre de la raza
        dog_breed = self.class_names['breeds'][pred[0].tolist().index(pred[0].max())]
        return dog_breed

