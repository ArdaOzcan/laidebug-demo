from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/", methods=["POST"])
def get():
    content = request.get_json(silent=True)
    if content == None:
        return jsonify({"error": {"message": "Invalid JSON."}, "id": None})

    print(content)
    return jsonify(content)
