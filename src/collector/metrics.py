"""Metrics collection for agent telemetry."""

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource


class AgentMetricsCollector:
    """Collect and export metrics for agent performance."""
    
    def __init__(self, service_name: str, endpoint: str = "http://localhost:4317"):
        """
        Initialize the metrics collector.
        
        Args:
            service_name: Name of the service collecting metrics
            endpoint: OTLP endpoint for metrics export
        """
        self.service_name = service_name
        
        # Set up metrics pipeline
        resource = Resource.create({"service.name": service_name})
        metric_reader = PeriodicExportingMetricReader(
            OTLPMetricExporter(endpoint=endpoint)
        )
        
        meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
        metrics.set_meter_provider(meter_provider)
        
        self.meter = metrics.get_meter(__name__)
        
        # Create metrics
        self.token_counter = self.meter.create_counter(
            name="agent.tokens",
            description="Number of tokens processed by the agent",
            unit="tokens",
        )
        
        self.latency_histogram = self.meter.create_histogram(
            name="agent.latency",
            description="Latency of agent operations",
            unit="ms",
        )
        
        self.error_counter = self.meter.create_counter(
            name="agent.errors",
            description="Number of errors encountered by the agent",
        )
        
    def record_tokens(self, count: int, attributes: dict = None):
        """
        Record token usage.
        
        Args:
            count: Number of tokens to record
            attributes: Additional attributes for the metric
        """
        self.token_counter.add(count, attributes or {})
        
    def record_latency(self, latency_ms: float, attributes: dict = None):
        """
        Record latency measurement.
        
        Args:
            latency_ms: Latency in milliseconds
            attributes: Additional attributes for the metric
        """
        self.latency_histogram.record(latency_ms, attributes or {})
        
    def record_error(self, error_type: str, attributes: dict = None):
        """
        Record an error occurrence.
        
        Args:
            error_type: Type of error encountered
            attributes: Additional attributes for the metric
        """
        attr = attributes or {}
        attr["error.type"] = error_type
        self.error_counter.add(1, attr)
