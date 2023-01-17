import tensorflow as tf

# batch de train y val deben ser iguales

def dataset(path_data, batch_size=None, img_h=228, img_w=228):
    train_ds, val_ds = tf.keras.utils.image_dataset_from_directory(
        path_data,
        seed=123,
        validation_split=0.3,
        subset="both",
        image_size=(img_h, img_w),
        batch_size=batch_size)
    class_names = train_ds.class_names

    train_ds = configure_for_performance(train_ds)
    counter = tf.data.Dataset.counter()
    train_ds = tf.data.Dataset.zip((train_ds, (counter, counter)))
    train_ds = (train_ds
        .map(augment, num_parallel_calls=tf.data.AUTOTUNE)
        .batch(32)
        .prefetch(tf.data.AUTOTUNE))
    val_ds = configure_for_performance(val_ds).batch(32)

    return train_ds, val_ds, class_names


def normalize_img(img, label):
    img = tf.cast(img, tf.float32)
    img = img / 255.0
    return img, label

def augment(image_label, seed):
    img, label = image_label
    new_seed = tf.random.experimental.stateless_split(seed, num=1)[0, :]
    #img = tf.image.resize_with_crop_or_pad(img, 228, 228)
    img = tf.image.stateless_random_flip_left_right(img, seed=new_seed)
    img = tf.image.stateless_random_flip_up_down(img, seed=new_seed)
    img = tf.image.stateless_random_crop(value=img, size=[180, 180, 3], seed=seed)
    return img, label

def configure_for_performance(ds):
    ds = ds.map(normalize_img, num_parallel_calls=tf.data.AUTOTUNE)
    ds = ds.shuffle(buffer_size=1000)
    ds = ds.prefetch(tf.data.AUTOTUNE)
    return ds



if __name__ == "__main":
    data_dir = "D_data/Images"
    batch_size = 32
    img_height = 180
    img_width = 180