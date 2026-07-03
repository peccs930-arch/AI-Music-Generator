```python
from music21 import converter

def load_midi(file_path):

    midi = converter.parse(file_path)

    return midi
```

