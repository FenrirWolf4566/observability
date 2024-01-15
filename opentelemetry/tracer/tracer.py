from flask import Flask, request, jsonify

app = Flask(__name__)

spans_infos_by_host = {} # link IP to a set of span names

@app.route('/', methods=['POST'])
def receive_traces():
    try:
        traces = request.get_json()

        if not traces:
            return jsonify(success=False, error="No traces received"), 400

        print("Traces received: "+str(len(traces)))
        for span_data in traces:
            ip_client = str(span_data['attributes']['origin']) if 'attributes' in span_data and 'origin' in span_data['attributes'] else "DEFAULT"
            if ip_client not in spans_infos_by_host:
                spans_infos_by_host[ip_client] = []
            span_name = str(span_data['name'])+"__0"
            if span_name in spans_infos_by_host[ip_client]:
                span_name = span_name[:-1] + str(int(spans_infos_by_host[ip_client][-1][-1])+1) # on incrémente le numéro précédent dans la liste
            spans_infos_by_host[ip_client].append(span_name)

            attributes_list = []
            if 'attributes' in span_data:
                for key, value in span_data['attributes'].items():
                    if key != "origin":
                        attributes_list.append(str(key) +","+ str(value))

            elapsed_time = str(span_data['end_time'] - span_data['start_time'])
            events = []
            if 'events' in span_data:
                for event in span_data['events']:
                    events.append(str(event["name"]) +","+ str(event['timestamp']))
            with open((ip_client.replace(".","_")+".csv"), 'a') as writer:
                writer.write(span_name +","+ elapsed_time +","+ " ".join(events) +","+ " ".join(attributes_list)+"\n")
        return jsonify(success=True)

    except Exception as e:
        print("FAILED with code : "+str(e))
        return jsonify(success=False, error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
