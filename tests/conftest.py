"""Test configuration for nexushive-agent-insights."""

import pytest
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider


@pytest.fixture(autouse=True)
def setup_opentelemetry():
    """Configure OpenTelemetry with no-op tracer for tests."""
    # Set up a no-op tracer provider to prevent real telemetry during tests
    trace.set_tracer_provider(TracerProvider())
    yield
    # Reset is not strictly necessary since each test has its own process,
    # but included for completeness
    trace._TRACER_PROVIDER = None