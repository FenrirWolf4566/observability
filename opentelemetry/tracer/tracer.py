from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_traces():
    try:
        traces = request.get_json()

        if not traces:
            return jsonify(success=False, error="No traces received"), 400

        print("Traces received:")
        for trace_name in traces:
            print(f"- {trace_name}")

        return jsonify(success=True)

    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)