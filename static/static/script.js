```javascript
const generateBtn = document.getElementById("generateBtn");

const statusText = document.getElementById("status");

const downloadBtn = document.getElementById("downloadBtn");


generateBtn.addEventListener("click", async () => {

    generateBtn.disabled = true;

    statusText.innerHTML =
        "🎵 AI is composing music... Please wait.";

    downloadBtn.style.display = "none";

    try {

        const response = await fetch("/generate", {

            method: "POST"

        });

        const data = await response.json();

        if (data.success) {

            statusText.innerHTML =
                "✅ Music generated successfully!";

            downloadBtn.href = data.file;

            downloadBtn.style.display = "inline-block";

        }

        else {

            statusText.innerHTML =
                "❌ " + data.message;

        }

    }

    catch (error) {

        statusText.innerHTML =
            "❌ Server Error.";

    }

    generateBtn.disabled = false;

});
```
