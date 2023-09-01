from GenerateCode import CodeGeneration
from Docker.DockerFunctions import DockerFunctions

if __name__ == "__main__":
    print("Initial testing with Docker...")
    python_code = "print('Hello from Docker!')"
    docker_test_result = DockerFunctions.run_python_in_docker(python_code)
    print(docker_test_result["info"])
    print(docker_test_result["status"])
    print(docker_test_result["code"])

    initial_prompt = input("Enter your function requirements for GPT-4: ")
    constructed_prompt = CodeGeneration.generate_function_prompt(initial_prompt)

    python_code = CodeGeneration.generate_code_from_user_prompt(constructed_prompt)
    result = DockerFunctions.run_python_in_docker(python_code)
    
    print("\nResults based on GPT-4 generated code:")
    print(result["info"])
    print(result["status"])
    print(result["code"])