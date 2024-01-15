from flask import Flask, request
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.exporter.zipkin.json import ZipkinExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
from opentelemetry.trace import Span, get_tracer_provider
import requests

import random as rd
import time

#######################################

class CustomExporter(SpanExporter):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def export(self, spans):
        try:
            # Convertir les spans en un format que votre serveur comprend
            formatted_spans = [self.format_spans(span) for span in spans]

            # Envoyer les spans à votre serveur Flask
            response = requests.post(self.endpoint, json=formatted_spans)

            # Gérer la réponse (optionnel)
            if response.status_code == 200:
                return SpanExportResult.SUCCESS
            else:
                return SpanExportResult.FAILURE

        except Exception as e:
            # Gérer les erreurs d'envoi (optionnel)
            print(f"Erreur lors de l'envoi des traces : {e}")
            return SpanExportResult.FAILURE

    def shutdown(self):
        pass  # Peut être utilisé pour effectuer des opérations de nettoyage lors de l'arrêt de l'application

    def format_spans(self, span):
        # Format spécifique de vos spans pour l'envoi au serveur Flask
        # Ici, on utilise simplement les noms des traces
        formatted_span = {
            'name': span.name,
            'start_time': span.start_time,
            'end_time': span.end_time,
            'events': [{
                'name': event.name,
                'attributes': dict(event.attributes) if hasattr(event, 'attributes') else None,
                'timestamp': event.timestamp if hasattr(event, 'timestamp') else None,
            } for event in span.events],
            'attributes': dict(span.attributes),
        }

        return formatted_span

#######################################


app = Flask(__name__)

# Exporter
exporter = CustomExporter(endpoint="http://10.0.0.251:5001/")

# Configurer le fournisseur de trace
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(SimpleSpanProcessor(exporter))
trace.set_tracer_provider(tracer_provider)

# Instrumenter Flask
FlaskInstrumentor().instrument_app(app)

def doSomething():
#Only sleep for a random generated time (from 10 to 999 ms)
#Create a nested span to indicate the time taken
    with trace.get_tracer(__name__).start_as_current_span("doSomething func") as child:
        current_span = trace.get_current_span()
        time_to_sleep = rd.randrange(10, 1000)/1000 # time to sleep in ms
        current_span.add_event("executing some diffuclt work (sleeping)")
        time.sleep(time_to_sleep)
        current_span.set_attribute("Time that the difficult work took",time_to_sleep)
        return


@app.route('/')
def hello():
    # Créer une nouvelle trace
    with trace.get_tracer(__name__).start_as_current_span("main func") as parent:
        current_span = trace.get_current_span()
        current_span.set_attribute('origin', request.remote_addr)
        current_span.set_attribute("description", "Will execute a set of random opperations to complete this span")
        rd_generated_number = rd.randrange(10)
        current_span.set_attribute("Random number [0,9]", rd_generated_number)

        if rd_generated_number%2 == 0:
            current_span.add_event("EVENT : Even number")
        else:
            current_span.add_event("EVENT : Odd number")

        start = time.time()
        doSomething()
        elapsed_time = time.time() - start
        current_span.set_attribute("Time in 'doSomething' function", elapsed_time)
        return "Hello, World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
