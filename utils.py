import re
import ast
import logging
import docker 

# Set up logging
logging.basicConfig(level=logging.INFO)

# FILE_INFO_MAPPING dictionary maps languages to their respective run commands and file extensions.
FILE_INFO_MAPPING = {
    'python': ('python', '.py'),
    'javascript': ('node', '.js'),
    'cpp': ('g++', '.cpp'),
    'java': ('java', '.java'),
    'jsx': ('node', '.jsx'),
    'php': ('php', '.php'),
    'swift': ('swift', '.swift'),
    'c#': ('dotnet', '.cs'),
    'go': ('go', '.go'),
}

# LANGUAGE_MAPPING dictionary maps languages to their respective docker image tags.
LANGUAGE_MAPPING = {
    'python': 'python:latest',
    'javascript': 'node:latest',
    'cpp': 'gcc:latest',
    'java': 'openjdk:latest',
    'jsx': 'node:latest',
    'php': 'php:latest',
    'swift': 'swift:latest',
    'c#': 'mcr.microsoft.com/dotnet/sdk:latest',
    'go': 'golang:latest',
}

# PACKAGE_INSTALLATION_COMMANDS dictionary maps languages to their respective package installation commands.
PACKAGE_INSTALLATION_COMMANDS = {
    "python": "pip install {}",
    "javascript": "npm install {}",
    "cpp": "apt-get install {}",
    "java": "apt-get install {}",
    "jsx": "npm install {}",
    "php": "composer require {}",
    "swift": "swift package add {}",
    "c#": "dotnet add package {}",
    "go": "go get {}",
}

def get_docker_image(language: str) -> str:
    """
    Returns the appropriate Docker image for a given language.
    """
    docker_image = LANGUAGE_MAPPING.get(language.lower())
    if not docker_image:
        raise ValueError(f"Unsupported language: {language}")
    return docker_image

def code_extractor(text: str) -> str:
    """
    Extracts code blocks encapsulated between ``` from a given text.
    """
    if not isinstance(text, str):
        raise TypeError("Input text must be string.")

    matches = re.findall(r'```(.*?)```', text, re.DOTALL)
    
    # Process matches to remove "python" from the first line, if present
    processed_matches = []
    for match in matches:
        lines = match.split('\n')
        if lines and "python" in lines[0].lower():
            lines = lines[1:]
        processed_matches.append('\n'.join(lines))

    return '\n'.join(processed_matches) if processed_matches else None


def package_extractor(s: str) -> list:
    """
    Extracts a list of packages from a string formatted as "[pkg1, pkg2, ...]".
    """
    match = re.search(r'\[[^\]]*\]', s)
    return ast.literal_eval(match.group()) if match else []

def execute_command_in_container(container, command: str) -> str:
    """
    Executes a command within a specified Docker container.
    """
    exit_code, output = container.exec_run(command)
    if exit_code != 0:
        raise RuntimeError(f"Command execution failed with exit code: {exit_code}. Output: {output.decode('utf-8').strip()}")
    return output.decode('utf-8').strip()

def install_packages(language: str, code: str, container_name: str) -> str:
    """
    Detect necessary packages for a given code in a particular language and install them in a Docker container.
    """
    if not language or not code:
        raise ValueError("Both language and code must be provided.")

    # Get the Docker image and client
    docker_image = get_docker_image(language)
    client = docker.from_env()

    # Note: The get_or_create_container function was not provided in the original code. Assuming it exists.
    container = get_or_create_container(client, docker_image, container_name)

    # Fetch the list of required packages for the given code
    packages = package_extractor(get_gpt4_completion(f"please write an array of packages [] required for this script {code}."))
    logging.info(f"Installing packages: {packages}")

    # Get the installation command template for the language
    installation_command = PACKAGE_INSTALLATION_COMMANDS.get(language.lower())
    if not installation_command:
        raise ValueError(f"Unsupported language: {language}")

    # Fill the template with the list of packages
    installation_command = installation_command.format(" ".join(packages))

    if not packages:
        return "No packages required"
    return execute_command_in_container(container, installation_command)