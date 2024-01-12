from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
from opentelemetry.trace import Span, get_tracer_provider

class CustomExporter(SpanExporter):
    def export(self, spans):
        # Logique d'exportation vers votre serveur Python
        for span in spans:
            # Envoyez chaque span à votre serveur
            print(f"Exporting span: {span.get_span_context()}")

        return SpanExportResult.SUCCESS
