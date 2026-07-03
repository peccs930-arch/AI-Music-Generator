```python
import os
import pickle

from music21 import converter
from music21 import instrument
from music21 import note
from music21 import chord

DATASET_PATH = "dataset"


def extract_notes():

    notes = []

    for file in os.listdir(DATASET_PATH):

        if not file.endswith(".mid"):
            continue

        print("Reading:", file)

        midi = converter.parse(
            os.path.join(DATASET_PATH, file)
        )

        try:

            parts = instrument.partitionByInstrument(midi)

            elements = parts.parts[0].recurse()

        except:

            elements = midi.flat.notes

        for element in elements:

            if isinstance(element, note.Note):

                notes.append(str(element.pitch))

            elif isinstance(element, chord.Chord):

                notes.append(
                    ".".join(
                        str(n)
                        for n in element.normalOrder
                    )
                )

    print("Total Notes:", len(notes))

    return notes


def save_notes(notes):

    with open("model/notes.pkl", "wb") as f:

        pickle.dump(notes, f)


def main():

    if not os.path.exists("model"):

        os.mkdir("model")

    notes = extract_notes()

    save_notes(notes)

    print("Notes saved successfully.")


if __name__ == "__main__":

    main()
```
