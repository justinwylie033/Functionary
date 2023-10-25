import unittest
from unittest.mock import Mock, patch, MagicMock
import logging
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO)

# Importing classes from utils.py
from utils import Utils, LanguageInfo

class TestUtilsCodeExtractor(unittest.TestCase):

    def test_code_extractor_valid_input(self) -> None:
        logging.info("Testing code extraction with valid input...")

        # Test extraction from a single code block
        input_text: str = "```python\nprint('Hello World')\n```"
        expected_output: str = "print('Hello World')\n"
        actual_output: str = Utils.code_extractor(input_text)
        self.assertEqual(expected_output, actual_output)

        # Test extraction from multiple code blocks
        input_text = """```python\nprint('Hello World')\n```
                       ```javascript\nconsole.log('Hello again');\n```"""
        expected_output = "print('Hello World')\n\nconsole.log('Hello again');\n"
        actual_output = Utils.code_extractor(input_text)
        self.assertEqual(expected_output, actual_output)

    def test_code_extractor_single_code_block(self) -> None:
        logging.info("Testing code extraction from a single code block...")

        input_text: str = "```python\nprint('Hello World')\n```"
        expected_output: str = "print('Hello World')\n"
        actual_output: str = Utils.code_extractor(input_text)
        self.assertEqual(expected_output, actual_output)

    def test_code_extractor_invalid_input(self) -> None:
        logging.info("Testing code extraction with invalid input...")

        input_text: Any = 12345
        expected_output: str = ""
        actual_output: str = Utils.code_extractor(input_text)
        self.assertEqual(expected_output, actual_output)

class TestUtilsExecuteCommand(unittest.TestCase):

    @patch('utils.logging.error')
    def test_execute_command_in_container(self, mock_logging_error: MagicMock) -> None:
        logging.info("Testing command execution in a container...")

        # Mock container with successful command execution
        mock_container: Mock = Mock()
        mock_container.exec_run.return_value = (0, b'Hello World')
        command: str = "echo Hello World"
        expected_output: str = "Hello World"
        actual_output: str = Utils.execute_command_in_container(mock_container, command)
        self.assertEqual(expected_output, actual_output)

        # Mock container with failed command execution
        mock_container.exec_run.return_value = (1, b'Error message')
        command = "exit 1"
        actual_output = Utils.execute_command_in_container(mock_container, command)
        self.assertIsNone(actual_output)

        # Mock container raising an exception
        mock_container.exec_run.side_effect = Exception("Docker exception")
        actual_output = Utils.execute_command_in_container(mock_container, command)
        self.assertIsNone(actual_output)

    def tearDown(self) -> None:
        """Clean up any objects/data after a test."""
        logging.info("Cleaning up after test...")

class TestLanguageInfo(unittest.TestCase):

    def test_language_details_properties(self):
        """Test that each language has the required properties."""
        for language, details in LanguageInfo.LANGUAGE_DETAILS.items():
            self.assertIn('interpreter', details)
            self.assertIn('extension', details)
            self.assertIn('docker_image', details)

            # Ensure extension starts with a dot
            self.assertTrue(details['extension'].startswith('.'))
            
    def test_invalid_language_descriptor(self):
        """Test code extraction with an invalid language descriptor."""
        input_text = "```invalidLang\nprint('This is invalid')\n```"
        expected_output = "invalidLang\nprint('This is invalid')\n"
        actual_output = Utils.code_extractor(input_text)
        self.assertEqual(expected_output, actual_output)


if __name__ == "__main__":
    unittest.main()
