from Docker.DockerFunctions import DockerFunctions
from PromptEngineering.prompts import Prompts
from Generation.Complete import get_gpt4_completion

def install_packages(code):
    package_install_prompt = Prompts.package_install(code)
    installation_command = get_gpt4_completion(package_install_prompt)
    print(installation_command)

    # Check for no packages required
    if "[]" in installation_command:
        print("No Packages Required")
        return

    # Attempt to install the packages
    if installation_command:
        docker_func = DockerFunctions()
        commands = installation_command.split('\n')
        for cmd in commands:
            try:
                docker_func.install_packages(cmd)
                print(f"'{cmd}' - Package Installed Successfully")
            except Exception as e:
                print(f"Failed to install with '{cmd}'. Error: {str(e)}")
    else:
        print("No installation command detected.")

def run_tests():
    # Test cases:
    
    # 1. Basic Python code that requires no packages.
    test_case_1 = "print('Hello World!')"
    
    # 2. Python code that requires a popular package.
    test_case_2 = "import requests\nresponse = requests.get('https://www.google.com')"
    
    # 3. JavaScript NodeJS code that requires a popular package.
    test_case_3 = "const express = require('express');\nconst app = express();"
    
    # 4. Python code that requires multiple packages.
    test_case_4 = "import requests, pandas\nresponse = requests.get('https://www.google.com')\ndf = pandas.DataFrame([1, 2, 3])"
    
    # 5. Java code to test if Java dependencies can be recognized.
    test_case_5 = "import org.apache.commons.lang3.StringUtils;\npublic class Test { public static void main(String[] args) { StringUtils.isBlank('Test'); } }"
    
    # 6. Ruby code for checking a popular gem.
    test_case_6 = "require 'sinatra'"
    
    # 7. R code to check if R libraries can be recognized.
    test_case_7 = "library(ggplot2)"
    
    # 8. A Perl script that uses a popular module.
    test_case_8 = "use LWP::Simple;\ngetprint('http://www.example.com');"
    
    # 9. PHP code that requires a popular package.
    test_case_9 = "<?php use GuzzleHttp\Client; ?>"
    
    # 10. A code snippet that doesn't correlate to any programming language.
    test_case_10 = "This is a test to check for invalid commands. Install using: nonsense_command package_name."

    test_cases = [
        test_case_1, test_case_2, test_case_3, test_case_4,
        test_case_5, test_case_6, test_case_7, test_case_8,
        test_case_9, test_case_10
    ]

    for idx, test_case in enumerate(test_cases, 1):
        print(f"Running test case {idx}...\n")
        install_packages(test_case)
        print("\n-------------------------\n")

if __name__ == "__main__":
    run_tests()
