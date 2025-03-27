# NexusHive Agent Insights

Enterprise-grade observability for AI agents using OpenTelemetry

## Overview

NexusHive Agent Insights provides comprehensive instrumentation, monitoring, and evaluation tools for AI agents, with a focus on the smolagents framework. Built on OpenTelemetry standards, it enables organizations to track critical agent metrics, evaluate performance, and ensure reliability in production environments.

## Features

- **OpenTelemetry Integration**: Seamlessly instrument agents with industry-standard telemetry
- **Comprehensive Metrics**: Track token usage, latency, errors, and custom KPIs
- **Real-time Evaluation**: Support for user feedback and LLM-as-judge evaluations
- **Offline Analysis**: Tools for benchmark testing (e.g., GSM8K) and performance comparison
- **smolagents Framework Support**: Built-in integration with smolagents architecture

## Use Cases

- **Agent Performance Tracking**: Monitor costs, response times, and success rates
- **Operational Oversight**: Identify errors and bottlenecks in agent deployments
- **Continuous Improvement**: Evaluate and refine agents based on real-world usage
- **Benchmark Testing**: Compare agent implementations against standard datasets

## Getting Started

```bash
# Install the package
pip install nexushive-agent-insights

# Basic usage
from nexushive.client import instrument_agent
from smolagents import Agent

# Instrument your agent
my_agent = Agent(...)
instrumented_agent = instrument_agent(my_agent)

# Use normally - telemetry is automatically collected
result = instrumented_agent.run(...)
```

## Project Structure

- `src/client/`: Agent instrumentation libraries
- `src/collector/`: Telemetry data collection and processing
- `src/examples/`: Usage examples and templates

## Resources

- [Hugging Face Agents Course](https://huggingface.co/learn/agents-course/unit2/smolagents/introduction)
- [Monitoring and Evaluating Agents](https://huggingface.co/learn/agents-course/bonus-unit2/monitoring-and-evaluating-agents-notebook)

## License

MIT License