import os
import zipfile

base_dir = 'E:\\Projects\\COD Target Trainer\\Training Data'
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')

# Directory with our training target pictures
train_targets_dir = os.path.join(train_dir, 'targets')

# Directory with our training neutral pictures
train_neutrals_dir = os.path.join(train_dir, 'neutral')

# Directory with our validation target pictures
validation_targets_dir = os.path.join(validation_dir, 'targets')

# Directory with our validation neutral pictures
validation_neutrals_dir = os.path.join(validation_dir, 'neutral')

train_target_fnames = os.listdir(train_targets_dir)
print(train_target_fnames[:10])

train_neutral_fnames = os.listdir(train_neutrals_dir)
train_neutral_fnames.sort()
print(train_neutral_fnames[:10])

print('total training targets images:', len(os.listdir(train_targets_dir)))
print('total training neutral images:', len(os.listdir(train_neutrals_dir)))
print('total validation targets images:', len(os.listdir(validation_targets_dir)))
print('total validation neutral images:', len(os.listdir(validation_neutrals_dir)))





import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Parameters for our graph; we'll output images in a 4x4 configuration
nrows = 4
ncols = 4

# Index for iterating over images
pic_index = 0

# Set up matplotlib fig, and size it to fit 4x4 pics
fig = plt.gcf()
fig.set_size_inches(ncols * 4, nrows * 4)

pic_index += 8
next_target_pix = [os.path.join(train_targets_dir, fname)
                for fname in train_target_fnames[pic_index-8:pic_index]]
next_neutral_pix = [os.path.join(train_neutrals_dir, fname)
                for fname in train_neutral_fnames[pic_index-8:pic_index]]

for i, img_path in enumerate(next_target_pix+next_neutral_pix):
  # Set up subplot; subplot indices start at 1
  sp = plt.subplot(nrows, ncols, i + 1)
  sp.axis('Off') # Don't show axes (or gridlines)

  img = mpimg.imread(img_path)
  plt.imshow(img)

#plt.show()

from tensorflow.keras import layers
from tensorflow.keras import Model

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
output = layers.Dense(1, activation='sigmoid')(x)

# Create model:
# input = input feature map
# output = input feature map + stacked convolution/maxpooling layers + fully
# connected layer + sigmoid output layer
model = Model(img_input, output)

model.summary()


from tensorflow.keras.optimizers import RMSprop

model.compile(loss='binary_crossentropy',
              optimizer=RMSprop(lr=0.001),
              metrics=['acc'])

from tensorflow.keras.preprocessing.image import ImageDataGenerator

# All images will be rescaled by 1./255
train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)

# Flow training images in batches of 20 using train_datagen generator
train_generator = train_datagen.flow_from_directory(
        train_dir,  # This is the source directory for training images
        target_size=(200, 200),  # All images will be resized to 200x200
        batch_size=20,
        # Since we use binary_crossentropy loss, we need binary labels
        class_mode='binary')

# Flow validation images in batches of 20 using val_datagen generator
validation_generator = val_datagen.flow_from_directory(
        validation_dir,
        target_size=(200, 200),
        batch_size=20,
        class_mode='binary')


import tensorflow as tf
import time
#tensor_board = tf.keras.callbacks.TensorBoard(log_dir=os.path.realpath('..')+"\\Logs\\{}".format(time.time()))

history = model.fit_generator(
      train_generator,
      steps_per_epoch=100,  # 2000 images = batch_size * steps
      epochs=10,
      #callbacks=[tensor_board],
      validation_data=validation_generator,
      validation_steps=50,  # 1000 images = batch_size * steps
      verbose=1)

model.save('E:\\Projects\\COD Target Trainer\\Training Data\\CODV5.h5')
