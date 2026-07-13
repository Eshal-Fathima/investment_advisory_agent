from flask import Flask, request, jsonify
from flask_cors import CORS

from crew import investment_crew

app = Flask(__name__)
CORS(app)  # allows the Vite dev server (localhost:5173) to call this API


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "question is required"}), 400

    result = investment_crew.kickoff(inputs={"question": question})

    return jsonify({"answer": str(result)})


if __name__ == "__main__":
    app.run(port=5000, debug=True)