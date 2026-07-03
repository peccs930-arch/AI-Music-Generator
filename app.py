```python
import os
import subprocess

from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import jsonify

app = Flask(__name__)

OUTPUT_FOLDER = "output"


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_music():

    try:

        subprocess.run(
            ["python", "generate.py"],
            check=True
        )

        return jsonify({

            "success": True,

            "message": "Music generated successfully.",

            "file": "/download/generated.mid"

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })


@app.route("/download/<filename>")
def download_file(filename):

    return send_from_directory(

        OUTPUT_FOLDER,

        filename,

        as_attachment=True

    )


if __name__ == "__main__":

    app.run(

        debug=True,

        port=5000

    )
```
