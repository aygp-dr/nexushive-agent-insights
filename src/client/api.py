"""Public API for agent instrumentation."""

from typing import Any, Callable, Optional, TypeVar, cast

from .instrumentation import AgentInstrumentor

T = TypeVar('T')


def instrument_agent(agent: T, 
                     service_name: str = "agent-service", 
                     agent_id: Optional[str] = None, 
                     endpoint: str = "http://localhost:4317") -> T:
    """
    Instrument an agent with OpenTelemetry tracing.
    
    This function patches the agent's run method to collect telemetry data
    including latency, token usage, and errors.
    
    Args:
        agent: The agent to instrument
        service_name: Name of the service running this agent
        agent_id: Optional unique identifier for this agent instance
        endpoint: OTLP endpoint for telemetry export
        
    Returns:
        The instrumented agent (same instance, modified in-place)
    """
    instrumentor = AgentInstrumentor(service_name, agent_id, endpoint)
    
    # Check if the agent has a run method
    if hasattr(agent, "run") and callable(getattr(agent, "run")):
        original_run = getattr(agent, "run")
        
        # Determine if async or sync
        if hasattr(original_run, "__await__"):
            wrapped_run = instrumentor.wrap_async_agent(original_run)
        else:
            wrapped_run = instrumentor.wrap_agent(original_run)
            
        # Replace the method
        setattr(agent, "run", wrapped_run)
    
    return agent
