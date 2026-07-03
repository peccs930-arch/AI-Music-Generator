```python
import pickle
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Activation

from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint

# --------------------------
# Load extracted notes
# --------------------------

with open("model/notes.pkl", "rb") as f:
    notes = pickle.load(f)

print("Total Notes:", len(notes))

# --------------------------
# Create vocabulary
# --------------------------

pitchnames = sorted(set(notes))

n_vocab = len(pitchnames)

print("Unique Notes:", n_vocab)

note_to_int = {
    note: number
    for number, note in enumerate(pitchnames)
}

# --------------------------
# Prepare sequences
# --------------------------

sequence_length = 100

network_input = []
network_output = []

for i in range(len(notes) - sequence_length):

    sequence_in = notes[i:i + sequence_length]

    sequence_out = notes[i + sequence_length]

    network_input.append(
        [note_to_int[n] for n in sequence_in]
    )

    network_output.append(
        note_to_int[sequence_out]
    )

n_patterns = len(network_input)

print("Training Patterns:", n_patterns)

# --------------------------
# Reshape input
# --------------------------

network_input = np.reshape(
    network_input,
    (n_patterns, sequence_length, 1)
)

network_input = network_input / float(n_vocab)

# --------------------------
# One-hot encode outputs
# --------------------------

network_output = to_categorical(
    network_output,
    num_classes=n_vocab
)

# --------------------------
# Build LSTM Model
# --------------------------

model = Sequential()

model.add(
    LSTM(
        512,
        input_shape=(network_input.shape[1],
                     network_input.shape[2]),
        return_sequences=True
    )
)

model.add(Dropout(0.3))

model.add(
    LSTM(
        512,
        return_sequences=True
    )
)

model.add(Dropout(0.3))

model.add(
    LSTM(
        512
    )
)

model.add(BatchNormalization())

model.add(Dropout(0.3))

model.add(
    Dense(256)
)

model.add(Activation("relu"))

model.add(
    Dense(n_vocab)
)

model.add(
    Activation("softmax")
)

model.compile(

    loss="categorical_crossentropy",

    optimizer="adam"

)

model.summary()

# --------------------------
# Save best model
# --------------------------

checkpoint = ModelCheckpoint(

    "model/music_model.keras",

    monitor="loss",

    verbose=1,

    save_best_only=True,

    mode="min"

)

callbacks = [checkpoint]

# --------------------------
# Train
# --------------------------

model.fit(

    network_input,

    network_output,

    epochs=50,

    batch_size=64,

    callbacks=callbacks

)

print("Training Completed")
```
