from keras import layers, Sequential
from keras.callbacks import EarlyStopping
from building_dataset import dataset
from GoogleDrive_API_connections.GDriveFunctions import search_file, download_file, upload_file
import os

path = "Weights/"
file_path = "classifier_weights.h5"
file_dir = path + file_path



def model_sequential(input_shape=(180, 180, 3), num_classes=120):
    model = Sequential(
        [
            layers.Conv2D(32, kernel_size=(3, 3), strides=1, padding="same", input_shape=input_shape, use_bias=False),
            layers.BatchNormalization(),
            layers.Activation("relu"),
            layers.MaxPooling2D(2, 2),
            layers.Conv2D(64, kernel_size=(3, 3), strides=1, padding="same", use_bias=False),
            layers.BatchNormalization(),
            layers.Activation("relu"),
            layers.MaxPooling2D(2, 2),
            layers.Conv2D(128, kernel_size=(3, 3), strides=1, padding="same", use_bias=False),
            layers.BatchNormalization(),
            layers.Activation("relu"),
            layers.MaxPooling2D(2, 2),
            layers.Conv2D(256, kernel_size=(3, 3), strides=1, padding="same", use_bias=False),
            layers.BatchNormalization(),
            layers.Activation("relu"),
            layers.MaxPooling2D(2, 2),
            layers.Conv2D(512, kernel_size=(3, 3), strides=1, padding="same", use_bias=False),
            layers.BatchNormalization(),
            layers.Activation("relu"),
            layers.MaxPooling2D(2, 2),
            layers.Flatten(),
            layers.Dropout(0.3),
            layers.Dense(256, activation="relu"),
            layers.Dropout(0.4),
            layers.Dense(512, activation="relu"),
            layers.Dropout(0.5),
            layers.Dense(num_classes, activation="softmax")
        ]
    )
    return model


def train_model(model, train_ds, val_ds, epochs=250, batch=32):
    early_stopping = EarlyStopping(
        min_delta=0.001, # minimium amount of change to count as an improvement
        patience=10, 
        restore_best_weights=True
    )

    model.compile(
        optimizer="adam",
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