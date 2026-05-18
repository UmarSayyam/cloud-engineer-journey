from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        "app":      "eks-api",
        "version":  "1.0"
    })

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json(silent=True) or {}
    return jsonify ({
        "received":     data,
        "processed":    True
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)