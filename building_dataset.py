import tensorflow as tf

def dataset(path_data, batch_size, img_h, img_w):
    train_ds, val_ds = tf.keras.utils.image_dataset_from_directory(
        path_data,
        seed=123,
        validation_split=0.3,
        subset="both",
        image_size=(img_h, img_w),
        batch_size=batch_size)
    class_names = train_ds.class_names

    return train_ds, val_ds, class_names

if __name__ == "__main":
    data_dir = "D_data/Images"
    batch_size = 32
    img_height = 180
    img_width = 180