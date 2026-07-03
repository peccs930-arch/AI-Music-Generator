```python
import pickle
import random
import numpy as np

from music21 import instrument
from music21 import note
from music21 import chord
from music21 import stream

from tensorflow.keras.models import load_model

# ----------------------------------
# Load trained model
# ----------------------------------

model = load_model("model/music_model.keras")

# ----------------------------------
# Load notes
# ----------------------------------

with open("model/notes.pkl", "rb") as f:
    notes = pickle.load(f)

pitchnames = sorted(set(notes))

n_vocab = len(pitchnames)

note_to_int = {
    note_name: number
    for number, note_name in enumerate(pitchnames)
}

int_to_note = {
    number: note_name
    for number, note_name in enumerate(pitchnames)
}

# ----------------------------------
# Prepare input sequences
# ----------------------------------

sequence_length = 100

network_input = []

for i in range(len(notes) - sequence_length):

    sequence = notes[i:i + sequence_length]

    network_input.append(
        [note_to_int[n] for n in sequence]
    )

# ----------------------------------
# Pick random seed
# ----------------------------------

start = random.randint(
    0,
    len(network_input) - 1
)

pattern = network_input[start]

prediction_output = []

print("Generating music...")

# ----------------------------------
# Generate 500 notes
# ----------------------------------

for _ in range(500):

    prediction_input = np.reshape(
        pattern,
        (1, len(pattern), 1)
    )

    prediction_input = prediction_input / float(n_vocab)

    prediction = model.predict(
        prediction_input,
        verbose=0
    )

    index = np.argmax(prediction)

    result = int_to_note[index]

    prediction_output.append(result)

    pattern.append(index)

    pattern = pattern[1:]

# ----------------------------------
# Convert notes to MIDI
# ----------------------------------

offset = 0

output_notes = []

for pattern in prediction_output:

    # Chord
    if "." in pattern or pattern.isdigit():

        notes_in_chord = pattern.split(".")

        chord_notes = []

        for current_note in notes_in_chord:

            new_note = note.Note(int(current_note))

            new_note.storedInstrument = instrument.Piano()

            chord_notes.append(new_note)

        new_chord = chord.Chord(chord_notes)

        new_chord.offset = offset

        output_notes.append(new_chord)

    # Single Note
    else:

        new_note = note.Note(pattern)

        new_note.offset = offset

        new_note.storedInstrument = instrument.Piano()

        output_notes.append(new_note)

    offset += 0.5

# ----------------------------------
# Create MIDI Stream
# ----------------------------------

midi_stream = stream.Stream(output_notes)

midi_stream.write(
    "midi",
    fp="output/generated.mid"
)

print("Music generated successfully!")
print("Saved as output/generated.mid")
```
