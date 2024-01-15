from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_traces():
    try:
        traces = request.get_json()

        if not traces:
            return jsonify(success=False, error="No traces received"), 400

        print("Traces received: "+str(len(traces)))
        for span_data in traces:
            print('#######################################################')
            print("Span name : ", str(span_data['name']))

            if 'attributes' in span_data:
                for key, value in span_data['attributes'].items():
                    print(str(key) + " : " + str(value))

            print("Start time : ", str(span_data['start_time']))
            print("End time : ", str(span_data['end_time']))
            if 'events' in span_data:
                for event in span_data['events']:
                    print("Span event : ", str(event))

        return jsonify(success=True)

    except Exception as e:
        print("FAILED with code : "+str(e))
        return jsonify(success=False, error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
