from Docker.DockerFunctions import DockerFunctions
from prompts import Prompts
from CodeGeneration.Completions import get_gpt4_completion

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
    
    # 1. Code that requires no packages.
    test_case_1 = "print('Hello World!')"
    
    # 2. Code that requires a popular package.
    test_case_2 = "import requests\nresponse = requests.get('https://www.google.com')"
    
    # 3. Code that requires a less common package.
    test_case_3 = "import obscure_package\nprint(obscure_package.function())"
    
    # 4. Code that requires multiple packages.
    test_case_4 = "import requests, pandas\nresponse = requests.get('https://www.google.com')\ndf = pandas.DataFrame([1, 2, 3])"
    
    # 5. A completely irrelevant text.
    test_case_5 = "This text should not trigger any installation."
    
    # 6. Code that is incorrectly formatted but should still trigger an installation command.
    test_case_6 = "import requests\n\nprint(;)"
    
    # 7. A valid code that results in an invalid installation command
    test_case_7 = "This is a test to check for invalid commands. Install using: nonsense_command package_name."
    
    # 8. Test with a known error
    test_case_8 = "Try installing 'fakepackage' which does not exist."

    test_cases = [
        test_case_1, test_case_2, test_case_3, test_case_4,
        test_case_5, test_case_6, test_case_7, test_case_8
    ]

    for idx, test_case in enumerate(test_cases, 1):
        print(f"Running test case {idx}...\n")
        install_packages(test_case)
        print("\n-------------------------\n")

if __name__ == "__main__":
    run_tests()
