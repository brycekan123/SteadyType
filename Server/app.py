from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load a pre-trained language model
corrector = pipeline("text2text-generation", model="t5-small")  # Small for lightweight inference

@app.route('/autocorrect', methods=['POST'])
def autocorrect():
    data = request.get_json()
    text = data.get("text", "")
    
    # Use the model to generate corrected text
    try:
        result = corrector(f"correct: {text}", max_length=50, num_return_sequences=1)
        corrected_text = result[0]['generated_text']
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"corrected_text": corrected_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
