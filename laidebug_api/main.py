from flask import Flask, request, jsonify
from flask_cors import CORS
import inspect
from laidebug_engine.core import debug_function

SUPPORTED_METHODS = {
    "debugFunction": debug_function,
}

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["POST"])
def get():
    content = request.get_json(silent=True)
    if content == None:
        return jsonify({"error": {"code": -32700, "message": "Invalid JSON."}, "id": None})

    if "id" not in content:
        return jsonify({"error": {"code": -32600, "message": "Invalid Request"}, "id": None})

    if "method" not in content or content["method"] not in SUPPORTED_METHODS:
        return jsonify({"error": {"code": -32601, "message": "Method not found"}, "id": content["id"]})

    if "params" not in content:
        return jsonify({"error": {"code": -32602, "message": "Invalid parameters."}, "id": content["id"]})

    method = SUPPORTED_METHODS[content["method"]]
    expected_args = len(inspect.signature(method).parameters)
    if len(content["params"]) != expected_args:
        return jsonify({"error": {"code": -32602, "message": "Invalid parameters."}, "id": content["id"]})

    try:
        result = method(*content["params"])
    except Exception as e:
        return jsonify({"error": {"code": -32603, "message": str(e)}, "id": content["id"]})

    return jsonify({"result": result, "id": content["id"]})
