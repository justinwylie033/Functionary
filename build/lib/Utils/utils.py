import re
import logging
from typing import Dict, Tuple, List, Any, Optional, Union

# Set up logging
logging.basicConfig(level=logging.INFO)


class LanguageInfo:
    """
    Class to encapsulate language related configurations.
    """
    
    # Constants for language mappings and file info.
    LANGUAGE_DETAILS: Dict[str, Dict[str, Union[str, Tuple[str, str]]]] = {
        'python': {'interpreter': 'python', 'extension': '.py', 'docker_image': 'python:latest'},
        'javascript': {'interpreter': 'node', 'extension': '.js', 'docker_image': 'node:latest'},
        'cpp': {'interpreter': 'g++', 'extension': '.cpp', 'docker_image': 'gcc:latest'},
        'java': {'interpreter': 'java', 'extension': '.java', 'docker_image': 'openjdk:latest'},
        'jsx': {'interpreter': 'node', 'extension': '.jsx', 'docker_image': 'node:latest'},
        'php': {'interpreter': 'php', 'extension': '.php', 'docker_image': 'php:latest'},
        'swift': {'interpreter': 'swift', 'extension': '.swift', 'docker_image': 'swift:latest'},
        'c#': {'interpreter': 'dotnet', 'extension': '.cs', 'docker_image': 'mcr.microsoft.com/dotnet/sdk:latest'},
        'go': {'interpreter': 'go', 'extension': '.go', 'docker_image': 'golang:latest'},
    }


class Utils:
    """
    Utility class containing static helper methods.
    """
    
    @staticmethod
    def code_extractor(text: str) -> str:
        """
        Extracts code blocks encapsulated between ``` from a given text.

        Args:
        - text (str): The input text containing code blocks.

        Returns:
        - str: Extracted code.
        """
        if not isinstance(text, str):
            logging.error("Input text must be string.")
            return ""

        matches = re.findall(r'```(.*?)```', text, re.DOTALL)
        
        # Process matches to remove the language descriptor from the first line
        processed_matches = []
        for match in matches:
            lines = match.split('\n')
            if lines and lines[0].lower() in LanguageInfo.LANGUAGE_DETAILS:  # Fix here
                lines = lines[1:]
            processed_matches.append('\n'.join(lines))

        return '\n'.join(processed_matches) if processed_matches else ""
    
    @staticmethod
    def execute_command_in_container(container: Any, command: str) -> Optional[str]:
        """
        Executes a command within a specified Docker container.

        Args:
        - container: The Docker container where the command should be executed.
        - command (str): The command to be executed.

        Returns:
        - str: Output of the executed command or None if there was an error.
        """
        try:
            exit_code, output = container.exec_run(command)
            if exit_code != 0:
                logging.error(f"Command execution failed with exit code: {exit_code}. Output: {output.decode('utf-8').strip()}")
                return None
            return output.decode('utf-8').strip()
        except Exception as e:
            logging.error(f"Error executing command in container: {e}")
            return None