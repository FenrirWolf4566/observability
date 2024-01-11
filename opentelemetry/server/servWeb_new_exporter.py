from flask import Flask
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.exporter.zipkin.json import ZipkinExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

app = Flask(__name__)

# CHANGE !!!
#zipkin_exporter = ZipkinExporter(endpoint="http://zipkin:9411/api/v2/spans")

# Configurer le fournisseur de trace
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(SimpleSpanProcessor(zipkin_exporter))
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