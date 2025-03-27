# Getting Started with NexusHive Agent Insights

This guide will help you set up and start using NexusHive Agent Insights for monitoring and evaluating your AI agents.

## Installation

Install the package using pip:

```bash
pip install nexushive-agent-insights
```

Or using Poetry:

```bash
poetry add nexushive-agent-insights
```

## Basic Usage

### Instrumenting an Agent

The simplest way to instrument an agent is to use the `instrument_agent` function:

```python
from nexushive.client import instrument_agent
from my_agent_package import MyAgent

# Create your agent
agent = MyAgent()

# Instrument the agent
instrumented_agent = instrument_agent(
    agent, 
    service_name="my-agent-service",
    agent_id="agent-001"  # Optional, defaults to a random UUID
)

# Use the instrumented agent normally
result = instrumented_agent.run("What's the weather in New York?")
```

This will automatically collect telemetry including:
- Latency measurements
- Token usage (input and output)
- Error tracking

### Setting up Telemetry Export

By default, telemetry is exported to an OpenTelemetry collector endpoint at `http://localhost:4317`. 
You can specify a different endpoint when instrumenting your agent:

```python
instrumented_agent = instrument_agent(
    agent, 
    service_name="my-agent-service",
    endpoint="https://my-otlp-endpoint:4317"
)
```

## Integration with smolagents

If you're using the smolagents framework, you can instrument your agents the same way:

```python
from nexushive.client import instrument_agent
from smolagents import Agent

agent = Agent(...)
instrumented_agent = instrument_agent(agent)

# Use as normal - telemetry is automatically collected
result = instrumented_agent.run(...)
```

## Viewing Telemetry Data

Telemetry data can be viewed in any OpenTelemetry-compatible observability platform such as:
- Jaeger
- Grafana
- Prometheus
- Datadog
- New Relic

## Next Steps

- Check out the [examples directory](../src/examples/) for more detailed usage patterns
- Read about [agent evaluation](./evaluation.md) using the evaluation modules
- Set up a complete [observability pipeline](./observability-pipeline.md) for production use