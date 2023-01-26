from keras import layers, Sequential
from keras.callbacks import EarlyStopping
from functools import partial
from building_dataset import dataset
from GoogleDrive_API_connections.GDriveFunctions import search_file, download_file, upload_file
import os

path = "Weights/"
file_path = "classifier_weights.h5"
file_dir = path + file_path


DefaultConv2D = partial(layers.Conv2D, kernel_size=3, strides=1, padding="same", use_bias=False)

class HiddenLayers(layers.Layer):
    def __init__(self, filters, strides=1, activation="relu", **kwargs):
        super().__init__(**kwargs)
        self.activation = layers.Activation(activation)
        self.main_layers = [
            DefaultConv2D(filters, strides=strides),
            layers.BatchNormalization(),
            self.activation,
            DefaultConv2D(filters),
            layers.BatchNormalization()]
        self.skip_layers = []
        if strides > 1:
            self.skip_layers = [
                DefaultConv2D(filters, kernel_size=1, strides=strides),
                layers.BatchNormalization()]

    def call(self, inputs):
        Z = inputs
        for layer in self.main_layers:
            Z = layer(Z)
        skip_Z = inputs
        for layer in self.skip_layers:
            skip_Z = layer(skip_Z)
        return self.activation(Z + skip_Z)


def model_sequential(input_shape=[180, 180, 3], num_classes=120):
    model = Sequential()
    model.add(
        DefaultConv2D(32, kernel_size=4, strides=2, input_shape=input_shape))
    model.add(
        layers.BatchNormalization())
    model.add(
        layers.Activation("relu"))
    model.add(
        layers.MaxPooling2D(pool_size=3, strides=2, padding="same"))
    prev_filters = 32
    for filters in [64] * 3 + [128] * 4 + [256] * 5:
        strides = 1 if filters == prev_filters else 2
        model.add(HiddenLayers(filters, strides=strides))
        prev_filters = filters
    model.add(
        layers.MaxPooling2D(pool_size=2, strides=2, padding="same"))
    model.add(
        layers.Dropout(0.2))
    model.add(
        layers.Conv2D(512, kernel_size=(3, 3), strides=1, padding="same", use_bias=False))
    model.add(
        layers.BatchNormalization())
    model.add(
        layers.Activation("relu"))
    model.add(
        layers.GlobalAvgPool2D())
    model.add(
        layers.Flatten())
    model.add(
        layers.Dropout(0.3))
    model.add(
        layers.Dense(256, activation="relu"))
    model.add(
        layers.Dropout(0.4))
    model.add(
        layers.Dense(512, activation="relu"))
    model.add(
        layers.Dropout(0.5))
    model.add(
        layers.Dense(num_classes, activation="softmax"))
    return model


def train_model(model, train_ds, val_ds, epochs=250, batch=16):
    early_stopping = EarlyStopping(
        min_delta=0.001, # minimium amount of change to count as an improvement
        patience=30, 
        restore_best_weights=True
    )

    model.compile(
        optimizer="sgd",
        loss="SparseCategoricalCrossentropy",
        metrics=["accuracy"]
    )

    model.fit(
        train_ds,
        validation_data=val_ds,
        batch_size=batch,
        epochs=epochs,
        callbacks=[early_stopping]
    )


if os.path.exists(path):
    print("Folder found")
    if os.path.exists(file_dir):
        print("File found, end")
    else:
        file = search_file(file_path)
        if len(file) <= 0:
            print("The file was not found in the cloud, creating it")
            data_dir = "D_data/Images"
            train_ds, val_ds, class_names = dataset(data_dir)
            model = model_sequential()
            train_model(model, train_ds, val_ds)
            model.save(file_dir)
            upload_file(file_path=file_dir)
        else:
            print("File found, downloading...")
            download_file(file_path, path)
else:
    print("The folder was not found, creating...")
    os.mkdir(path)
    print("Successfully created folder")
    file = search_file(file_path)
    if len(file) <= 0:
        print("The file was not found in the cloud, creating it")
        data_dir = "D_data/Images"
        train_ds, val_ds, class_names = dataset(data_dir)
        model = model_sequential()
        train_model(model, train_ds, val_ds)
        model.save(file_dir)
        upload_file(file_path=file_dir)
    else:
        print("File found, downloading...")
        download_file(file_path, path)