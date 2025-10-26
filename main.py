from flask import Flask, render_template_string, request
import PyPDF2
import os
import re
import time

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PDF Analyzer</title>
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Poppins', sans-serif;
    }

    body {
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        background: radial-gradient(circle at top left, #1a0000, #330000, #660000);
        color: white;
        overflow: hidden;
    }

    .container {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 40px 30px;
        width: 400px;
        max-width: 90%;
        text-align: center;
        box-shadow: 0 0 25px rgba(255, 0, 0, 0.4);
        animation: fadeIn 1s ease forwards;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }

    h1 {
        color: #ff4d4d;
        font-size: 1.8em;
        margin-bottom: 25px;
        text-shadow: 0 0 8px #ff0000;
    }

    input[type=file] {
        display: none;
    }

    label {
        display: inline-block;
        padding: 12px 25px;
        background: #ff0000;
        color: white;
        border-radius: 30px;
        cursor: pointer;
        transition: 0.3s;
        font-weight: bold;
        font-size: 1em;
    }

    label:hover {
        background: #ff3333;
        box-shadow: 0 0 12px #ff0000;
    }

    .filename {
        margin-top: 12px;
        font-size: 0.9em;
        color: #ffb3b3;
        word-wrap: break-word;
    }

    button {
        margin-top: 25px;
        background: #ff1a1a;
        border: none;
        padding: 12px 30px;
        border-radius: 30px;
        color: white;
        font-weight: bold;
        cursor: pointer;
        transition: 0.3s;
        font-size: 1em;
    }

    button:hover {
        background: #ff3333;
        box-shadow: 0 0 15px #ff0000;
    }

    .loader {
        display: none;
        border: 4px solid rgba(255, 255, 255, 0.2);
        border-left-color: #ff3333;
        border-radius: 50%;
        width: 45px;
        height: 45px;
        margin: 20px auto;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        100% { transform: rotate(360deg); }
    }

    .result {
        margin-top: 25px;
        font-size: 1.1em;
        color: #ff9999;
        text-shadow: 0 0 5px #ff0000;
        opacity: 0;
        animation: fadeInText 1s forwards;
    }

    @keyframes fadeInText {
        to { opacity: 1; transform: translateY(0); }
    }

    footer {
        position: fixed;
        bottom: 10px;
        font-size: 0.9em;
        color: rgba(255,255,255,0.7);
        letter-spacing: 1px;
        text-align: center;
        width: 100%;
    }

    /* 📱 Responsive Design */
    @media (max-width: 600px) {
        .container {
            width: 90%;
            padding: 30px 20px;
        }
        h1 {
            font-size: 1.5em;
        }
        label, button {
            width: 100%;
            font-size: 1em;
            padding: 12px 0;
        }
        .result {
            font-size: 1em;
        }
    }
</style>
</head>
<body>
    <div class="container">
        <h1>PDF Analyzer</h1>
        <form id="pdfForm" method="POST" enctype="multipart/form-data">
            <input type="file" name="pdf_file" id="pdf_file" accept=".pdf" required>
            <label for="pdf_file">Choose PDF</label>
            <div id="fileName" class="filename"></div>
            <button type="submit" id="countBtn">Analyze PDF</button>
        </form>
        <div class="loader" id="loader"></div>

        {% if word_count is not none %}
        <div class="result">
            📝 <b>Total Words:</b> {{ word_count }}<br>
            📖 <b>Total Sentences:</b> {{ sentence_count }}
        </div>
        {% endif %}
    </div>
    <footer>Created by <b>Dilkash</b></footer>

<script>
    const fileInput = document.getElementById("pdf_file");
    const fileName = document.getElementById("fileName");
    const loader = document.getElementById("loader");
    const form = document.getElementById("pdfForm");

    fileInput.addEventListener("change", () => {
        if (fileInput.files.length > 0) {
            fileName.textContent = "📄 " + fileInput.files[0].name;
        } else {
            fileName.textContent = "";
        }
    });

    form.addEventListener("submit", () => {
        loader.style.display = "block";
    });
</script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    word_count = None
    sentence_count = None
    if request.method == "POST":
        pdf = request.files["pdf_file"]
        if pdf and pdf.filename.endswith(".pdf"):
            path = "temp.pdf"
            pdf.save(path)
            try:
                with open(path, "rb") as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() or ""
                    words = text.split()
                    sentences = re.split(r'[.!?]+', text)
                    word_count = len(words)
                    sentence_count = len([s for s in sentences if s.strip()])
                    time.sleep(1)  # loader animation delay
            except Exception as e:
                word_count = "Error"
                sentence_count = "Error"
            finally:
                os.remove(path)
    return render_template_string(html, word_count=word_count, sentence_count=sentence_count)

if __name__ == "__main__":
    app.run(debug=True)
