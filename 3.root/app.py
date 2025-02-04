from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload():
    data = request.data

    try:
        # Deserialize the data (VULNERABLE)
        obj = pickle.loads(data)
        return jsonify({"message": "Data processed successfully!", "data": str(obj)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
