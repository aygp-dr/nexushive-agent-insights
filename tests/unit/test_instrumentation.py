"""Tests for agent instrumentation."""

import time
import unittest
from unittest.mock import MagicMock, patch

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

from nexushive.client.instrumentation import AgentInstrumentor


class TestAgentInstrumentor(unittest.TestCase):
    """Test the AgentInstrumentor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Configure a no-op tracer for testing
        trace.set_tracer_provider(TracerProvider())
    
    def test_wrap_agent(self):
        """Test that wrap_agent correctly instruments a function."""
        instrumentor = AgentInstrumentor("test-service", "test-agent-id")
        
        # Create a mock function
        mock_run = MagicMock(return_value="test response")
        
        # Wrap the function
        wrapped_run = instrumentor.wrap_agent(mock_run)
        
        # Call the wrapped function
        result = wrapped_run("test input")
        
        # Check that the original function was called
        mock_run.assert_called_once_with("test input")
        
        # Check that the result is correct
        self.assertEqual(result, "test response")
    
    @patch('time.time')
    def test_latency_measurement(self, mock_time):
        """Test that the wrapper measures latency."""
        # Configure mock time.time() to return sequence of values
        mock_time.side_effect = [100.0, 100.5]  # 500ms difference
        
        instrumentor = AgentInstrumentor("test-service", "test-agent-id")
        
        # Create a spy tracer to check span attributes
        tracer_spy = MagicMock()
        instrumentor.tracer = tracer_spy
        
        # Mock span context manager
        mock_span = MagicMock()
        tracer_spy.start_as_current_span.return_value.__enter__.return_value = mock_span
        
        # Create and wrap a function
        def test_func():
            return "test"
        
        wrapped_func = instrumentor.wrap_agent(test_func)
        
        # Call the wrapped function
        wrapped_func()
        
        # Check that latency was recorded
        mock_span.set_attribute.assert_any_call("agent.latency_ms", 500.0)
    
    def test_error_handling(self):
        """Test that errors are properly recorded."""
        instrumentor = AgentInstrumentor("test-service", "test-agent-id")
        
        # Create a spy tracer to check span attributes
        tracer_spy = MagicMock()
        instrumentor.tracer = tracer_spy
        
        # Mock span context manager
        mock_span = MagicMock()
        tracer_spy.start_as_current_span.return_value.__enter__.return_value = mock_span
        
        # Create a function that raises an exception
        def error_func():
            raise ValueError("test error")
        
        wrapped_func = instrumentor.wrap_agent(error_func)
        
        # Call the wrapped function and expect an exception
        with self.assertRaises(ValueError):
            wrapped_func()
        
        # Check that the error was recorded
        mock_span.record_exception.assert_called_once()
        mock_span.set_attribute.assert_any_call("agent.error", "test error")


if __name__ == "__main__":
    unittest.main()
