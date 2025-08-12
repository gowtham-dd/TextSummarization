from flask import Flask, render_template, request, jsonify
from TextSummarization.pipeline.prediction import PredictionPipeline
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", summary="", original_text="")

@app.route("/train", methods=["GET"])
def train():
    try:
        os.system("python main.py")
        return "Training successful !!"
    except Exception as e:
        return f"Error Occurred! {e}"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_text = request.form.get("input_text", "").strip()

        # If no input, return appropriate response for AJAX
        if not input_text:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"error": "No text provided"}), 400
            return render_template("index.html", summary="⚠ Please enter text to summarize", original_text="")

        obj = PredictionPipeline()
        summary = obj.predict(input_text)

        # If AJAX request, return JSON only (so client injects summary text)
        if request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json:
            return jsonify({"summary": summary})

        # Fallback (form submit without JS): render full page
        return render_template("index.html", summary=summary, original_text=input_text)

    except Exception as e:
        # Return JSON error for AJAX
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"error": str(e)}), 500
        raise e

if __name__ == "__main__":
    app.run(debug=True, port=8080)
