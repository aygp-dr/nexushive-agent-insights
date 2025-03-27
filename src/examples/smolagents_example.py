"""Example of instrumenting a smolagents agent."""

# This is a placeholder that demonstrates the API
# Actual implementation would depend on smolagents version and structure

from nexushive.client import instrument_agent

# Placeholder for smolagents import
# from smolagents import Agent


def main():
    """Run an example with an instrumented agent."""
    # Create a mock agent class for demonstration
    class MockAgent:
        def __init__(self, name):
            self.name = name
        
        def run(self, input_text):
            """Process the input and return a response."""
            # In a real agent, this would call LLMs, tools, etc.
            return f"Response from {self.name} to: {input_text}"

    # Create and instrument the agent
    agent = MockAgent("DemoAgent")
    instrumented_agent = instrument_agent(
        agent, 
        service_name="demo-agent-service",
        agent_id="demo-1"
    )
    
    # Use the agent as normal - telemetry is automatically collected
    result = instrumented_agent.run("Hello, agent!")
    print(result)


if __name__ == "__main__":
    main()
