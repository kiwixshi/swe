import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import InceptionV3, EfficientNetB5
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, BatchNormalization, Dropout, Input, Concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import AdamW
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.regularizers import l2

# Define the path to the pics directory
data_dir = r'C:\mine\swe\pics'

# Input layer
input_tensor = Input(shape=(380, 380, 3))

# Load Pretrained InceptionV3 model (without top layers)
inception_model = InceptionV3(weights='imagenet', include_top=False, input_tensor=input_tensor)

# Load Pretrained EfficientNetB5 model (without top layers)
efficientnet_model = EfficientNetB5(weights='imagenet', include_top=False, input_tensor=input_tensor)

# Global Average Pooling for both models
inception_output = GlobalAveragePooling2D()(inception_model.output)
efficientnet_output = GlobalAveragePooling2D()(efficientnet_model.output)

# Concatenate the outputs from both networks
combined = Concatenate()([inception_output, efficientnet_output])

# Add custom layers on top of the combined outputs
x = BatchNormalization()(combined)  # Batch Normalization
x = Dense(1024, activation='relu', kernel_regularizer=l2(0.001))(x)  # Fully connected layer with L2 regularization
x = Dropout(0.5)(x)  # Dropout to reduce overfitting
predictions = Dense(7, activation='softmax')(x)  # 7 classes for classification

# Create the final model
model = Model(inputs=input_tensor, outputs=predictions)

# Freeze the base layers to avoid retraining them initially
for layer in inception_model.layers:
    layer.trainable = False
for layer in efficientnet_model.layers:
    layer.trainable = False

# Compile the model with AdamW optimizer and categorical cross-entropy loss
model.compile(optimizer=AdamW(learning_rate=0.0001, weight_decay=1e-5), loss='categorical_crossentropy', metrics=['accuracy'])

# Data augmentation and preprocessing
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=60,         # Increased rotation range
    width_shift_range=0.4,     # Increased width shift
    height_shift_range=0.4,    # Increased height shift
    shear_range=0.4,           # Shear transformations
    zoom_range=0.4,            # Random zoom
    horizontal_flip=True,      # Random horizontal flips
    brightness_range=[0.7, 1.3],  # More aggressive brightness changes
    fill_mode='nearest',       # Fill any missing pixels
    validation_split=0.2       # Split data for validation (20%)
)

# Training generator
train_generator = train_datagen.flow_from_directory(
    data_dir,
    target_size=(380, 380),  # Image size 380x380
    batch_size=32,
    class_mode='categorical',
    subset='training'        # Use the training subset
)

# Validation generator
validation_generator = train_datagen.flow_from_directory(
    data_dir,
    target_size=(380, 380),
    batch_size=32,
    class_mode='categorical',
    subset='validation'      # Use the validation subset
)

# Callbacks for early stopping and learning rate adjustment
early_stopping = EarlyStopping(monitor='val_loss', patience=7, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-7)

# Train the model
model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=20,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    validation_steps=validation_generator.samples // validation_generator.batch_size,
    callbacks=[early_stopping, reduce_lr]
)

# Fine-tuning: Unfreeze layers of both Inception and EfficientNet models
for layer in inception_model.layers[-20:]:  # Unfreeze last 20 layers of Inception
    layer.trainable = True
for layer in efficientnet_model.layers[-20:]:  # Unfreeze last 20 layers of EfficientNet
    layer.trainable = True

# Compile and fine-tune with an even lower learning rate
model.compile(optimizer=AdamW(learning_rate=1e-6, weight_decay=1e-6), loss='categorical_crossentropy', metrics=['accuracy'])

# Fine-tune the model
model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=10,  # Fine-tune for more epochs
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    validation_steps=validation_generator.samples // validation_generator.batch_size,
    callbacks=[early_stopping, reduce_lr]
)

# Save the fine-tuned model
model.save('combined_inception_efficientnet_classifier.h5')
