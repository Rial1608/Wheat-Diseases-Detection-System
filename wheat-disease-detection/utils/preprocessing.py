import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os


def create_train_data_generator():
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2,
        fill_mode='nearest'
    )
    return train_datagen


def create_val_data_generator():
    val_datagen = ImageDataGenerator(rescale=1./255)
    return val_datagen


def load_training_data(train_dir, batch_size=32, target_size=(224, 224)):
    train_datagen = create_train_data_generator()
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='categorical'
    )
    return train_generator


def load_validation_data(val_dir, batch_size=32, target_size=(224, 224)):
    val_datagen = create_val_data_generator()
    val_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='categorical'
    )
    return val_generator


def load_test_data(test_dir, batch_size=32, target_size=(224, 224)):
    test_datagen = create_val_data_generator()
    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False
    )
    return test_generator


def get_class_labels(data_dir):
    classes = sorted(os.listdir(data_dir))
    return {i: cls for i, cls in enumerate(classes)}
