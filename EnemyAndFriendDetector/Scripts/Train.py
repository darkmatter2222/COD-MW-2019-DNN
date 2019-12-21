import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from tensorflow.keras import layers
from tensorflow.keras import Model
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import time

# Pull in all data
base_dir = 'E:\\Projects\\COD Enemy And Friendly Trainer\\Training Data'
train_dir = os.path.join(base_dir, 'Train')
validation_dir = os.path.join(base_dir, 'Validation')

# Directory with our training enemies pictures
train_enemies_dir = os.path.join(train_dir, 'Enemy')
# Directory with our training neutral pictures
train_neutrals_dir = os.path.join(train_dir, 'Neutral')
# Directory with our training friends pictures
train_friends_dir = os.path.join(train_dir, 'Friend')

# Directory with our validation enemies pictures
validation_enemies_dir = os.path.join(validation_dir, 'Enemy')
# Directory with our validation neutral pictures
validation_neutrals_dir = os.path.join(validation_dir, 'Neutral')
# Directory with our validation neutral pictures
validation_friends_dir = os.path.join(validation_dir, 'Friend')

train_enemies = os.listdir(train_enemies_dir)
print(train_enemies[:1])
train_neutral = os.listdir(train_neutrals_dir)
print(train_neutral[:1])
train_friends = os.listdir(train_friends_dir)
print(train_friends[:1])

print('total training enemies images:', len(os.listdir(train_enemies_dir)))
print('total training neutral images:', len(os.listdir(train_neutrals_dir)))
print('total training friends images:', len(os.listdir(train_friends_dir)))
print('total validation enemies images:', len(os.listdir(validation_enemies_dir)))
print('total validation neutral images:', len(os.listdir(validation_neutrals_dir)))
print('total validation friends images:', len(os.listdir(validation_friends_dir)))

# Our input feature map is 200x200x3: 200x200 for the image pixels, and 3 for
# the three color channels: R, G, and B
img_input = layers.Input(shape=(200, 200, 3))

# First convolution extracts 16 filters that are 3x3
# Convolution is followed by max-pooling layer with a 2x2 window
x = layers.Conv2D(16, 3, activation='relu')(img_input)
x = layers.MaxPooling2D(2)(x)

# Second convolution extracts 32 filters that are 3x3
# Convolution is followed by max-pooling layer with a 2x2 window
x = layers.Conv2D(32, 3, activation='relu')(x)
x = layers.MaxPooling2D(2)(x)

# Third convolution extracts 64 filters that are 3x3
# Convolution is followed by max-pooling layer with a 2x2 window
x = layers.Conv2D(64, 3, activation='relu')(x)
x = layers.MaxPooling2D(2)(x)

# Flatten feature map to a 1-dim tensor so we can add fully connected layers
x = layers.Flatten()(x)

# Create a fully connected layer with ReLU activation and 512 hidden units
x = layers.Dense(512, activation='relu')(x)

# Create output layer with a single node and sigmoid activation
output = layers.Dense(3, activation='sigmoid')(x)

# Create model:
# input = input feature map
# output = input feature map + stacked convolution/maxpooling layers + fully
# connected layer + sigmoid output layer
model = Model(img_input, output)

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(lr=0.001),
              metrics=['acc'])


# All images will be rescaled by 1./255
train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)

# Flow training images in batches of 20 using train_datagen generator
train_generator = train_datagen.flow_from_directory(
        train_dir,  # This is the source directory for training images
        target_size=(200, 200),  # All images will be resized to 200x200
        batch_size=5,
        # Since we use binary_crossentropy loss, we need binary labels
        class_mode='categorical')

# Flow validation images in batches of 20 using val_datagen generator
validation_generator = val_datagen.flow_from_directory(
        validation_dir,
        target_size=(200, 200),
        batch_size=5,
        class_mode='categorical')

tensor_board = tf.keras.callbacks.TensorBoard(log_dir=os.path.realpath('..')+"\\Logs\\{}".format(time.time()))

classes = train_generator.class_indices
print(classes)

history = model.fit_generator(
      train_generator,
      steps_per_epoch=100,  # 2000 images = batch_size * steps
      epochs=2,
      callbacks=[tensor_board],
      validation_data=validation_generator,
      validation_steps=1,  # 1000 images = batch_size * steps
      verbose=1)



model.save('E:\\Projects\\COD Enemy And Friendly Trainer\\Models\\MultiClassV2.h5')
