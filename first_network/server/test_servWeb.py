from flask import Flask
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.exporter.zipkin.json import ZipkinExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
from opentelemetry.trace import Span, get_tracer_provider
import requests

#######################################

class CustomExporter(SpanExporter):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def export(self, spans):
	print(spans)
        try:
            # Convertir les spans en un format que votre serveur comprend
            formatted_spans = self.format_spans(spans)

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

    def format_spans(self, spans):
        # Format spécifique de vos spans pour l'envoi au serveur Flask
        # Ici, on utilise simplement les noms des traces
        return [span.name for span in spans]

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

@app.route('/')
def hello():
    # Créer une nouvelle trace
    with trace.get_tracer(__name__).start_as_current_span("hello"):
        return "Hello, World!"

if __name__ == '__main__':
    nbRequests = 0
    app.run(host='0.0.0.0', port=5000, debug=True)
