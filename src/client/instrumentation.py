"""Agent instrumentation utilities."""

import time
import uuid
from typing import Any, Callable, Awaitable

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter


class AgentInstrumentor:
    """Instrument AI agents with OpenTelemetry tracing."""

    def __init__(self, service_name: str, agent_id: str = None, endpoint: str = "http://localhost:4317"):
        """
        Initialize the agent instrumentor.
        
        Args:
            service_name: The name of the service
            agent_id: Unique identifier for this agent
            endpoint: OTLP endpoint for exporting telemetry
        """
        self.agent_id = agent_id or str(uuid.uuid4())
        
        resource = Resource.create({
            "service.name": service_name,
            "agent.id": agent_id
        })
        
        trace_provider = TracerProvider(resource=resource)
        otlp_exporter = OTLPSpanExporter(endpoint=endpoint)
        trace_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
        trace.set_tracer_provider(trace_provider)
        
        self.tracer = trace.get_tracer(__name__)
    
    def wrap_agent(self, run_func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Wrap any agent's run function with telemetry
        
        Args:
            run_func: The agent's run function to wrap
            
        Returns:
            A wrapped function that records telemetry
        """
        def wrapped_run(*args, **kwargs):
            with self.tracer.start_as_current_span("agent.run") as span:
                start_time = time.time()
                
                # Add basic attributes
                span.set_attribute("agent.id", self.agent_id)
                
                # Count input tokens if possible
                input_text = kwargs.get("input", "")
                if isinstance(input_text, str):
                    input_tokens = len(input_text.split())
                    span.set_attribute("agent.tokens.input", input_tokens)
                
                try:
                    # Run the original function
                    result = run_func(*args, **kwargs)
                    
                    # Record output tokens if result is a string
                    if isinstance(result, str):
                        output_tokens = len(result.split())
                        span.set_attribute("agent.tokens.output", output_tokens)
                    
                    return result
                    
                except Exception as e:
                    span.record_exception(e)
                    span.set_attribute("agent.error", str(e))
                    raise
                finally:
                    # Calculate and record latency
                    latency_ms = (time.time() - start_time) * 1000
                    span.set_attribute("agent.latency_ms", latency_ms)
        
        return wrapped_run
    
    def wrap_async_agent(self, run_func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        """
        Wrap any agent's async run function with telemetry
        
        Args:
            run_func: The agent's async run function to wrap
            
        Returns:
            A wrapped async function that records telemetry
        """
        async def wrapped_run(*args, **kwargs):
            with self.tracer.start_as_current_span("agent.run") as span:
                start_time = time.time()
                
                # Add basic attributes
                span.set_attribute("agent.id", self.agent_id)
                
                # Count input tokens if possible
                input_text = kwargs.get("input", "")
                if isinstance(input_text, str):
                    input_tokens = len(input_text.split())
                    span.set_attribute("agent.tokens.input", input_tokens)
                
                try:
                    # Run the original function
                    result = await run_func(*args, **kwargs)
                    
                    # Record output tokens if result is a string
                    if isinstance(result, str):
                        output_tokens = len(result.split())
                        span.set_attribute("agent.tokens.output", output_tokens)
                    
                    return result
                    
                except Exception as e:
                    span.record_exception(e)
                    span.set_attribute("agent.error", str(e))
                    raise
                finally:
                    # Calculate and record latency
                    latency_ms = (time.time() - start_time) * 1000
                    span.set_attribute("agent.latency_ms", latency_ms)
        
        return wrapped_run
