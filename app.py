from flask import Flask, request, jsonify
from flask_cors import CORS
from mistral import (
    get_interactions,
    get_dosage_safety,
    get_clinical_warnings,
    get_recommendations
)

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    drugs = data.get("drugs", [])

    if not drugs:
        return jsonify({"error": "No drug data provided."}), 400

    return jsonify({
        "interactions": get_interactions(drugs),
        "dosage_safety": get_dosage_safety(drugs),
        "clinical_warnings": get_clinical_warnings(drugs),
        "recommendations": get_recommendations(drugs)
    })

if __name__ == '__main__':
    app.run(debug=True)
