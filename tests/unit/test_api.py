"""Tests for the public API."""

import unittest
from unittest.mock import MagicMock, patch

from nexushive.client.api import instrument_agent


class TestApiInstrument(unittest.TestCase):
    """Test the instrument_agent function."""
    
    @patch('nexushive.client.api.AgentInstrumentor')
    def test_instrument_sync_agent(self, mock_instrumentor_class):
        """Test instrumenting a synchronous agent."""
        # Set up mock
        mock_instrumentor = MagicMock()
        mock_instrumentor_class.return_value = mock_instrumentor
        
        mock_wrapped_run = MagicMock()
        mock_instrumentor.wrap_agent.return_value = mock_wrapped_run
        
        # Create a test agent class
        class TestAgent:
            def run(self, input_text):
                return f"Response to: {input_text}"
        
        # Instrument the agent
        agent = TestAgent()
        instrumented_agent = instrument_agent(agent, "test-service")
        
        # Check that the agent was instrumented
        self.assertIs(instrumented_agent, agent)  # Should modify in place
        mock_instrumentor.wrap_agent.assert_called_once_with(agent.run)
        self.assertEqual(agent.run, mock_wrapped_run)
    
    @patch('nexushive.client.api.AgentInstrumentor')
    def test_instrument_async_agent(self, mock_instrumentor_class):
        """Test instrumenting an asynchronous agent."""
        # Set up mock
        mock_instrumentor = MagicMock()
        mock_instrumentor_class.return_value = mock_instrumentor
        
        mock_wrapped_run = MagicMock()
        mock_instrumentor.wrap_async_agent.return_value = mock_wrapped_run
        
        # Create a test agent class with an async run method
        class TestAsyncAgent:
            async def run(self, input_text):
                return f"Response to: {input_text}"
        
        # Make the run method look async to our detection logic
        TestAsyncAgent.run.__await__ = MagicMock()  # type: ignore
        
        # Instrument the agent
        agent = TestAsyncAgent()
        instrumented_agent = instrument_agent(agent, "test-service")
        
        # Check that the agent was instrumented
        self.assertIs(instrumented_agent, agent)  # Should modify in place
        mock_instrumentor.wrap_async_agent.assert_called_once_with(agent.run)
        self.assertEqual(agent.run, mock_wrapped_run)


if __name__ == "__main__":
    unittest.main()