from Generate import Generation
from Docker.DockerFunctions import DockerFunctions

if __name__ == "__main__":
    DockerFunctions.set_language("python")
    print("Initial testing with Docker...")
    python_code = "print('Hello from Docker!')"
    print(python_code)
    docker_test_result = DockerFunctions.run_code_in_docker(python_code)
    print(docker_test_result["info"])
    print(docker_test_result["status"])
    print(docker_test_result["code"])

    initial_prompt = input("Enter your function requirements for GPT-4: ")
    constructed_prompt = Generation.generate_function_prompt(initial_prompt)

    python_code = Generation.generate_code_from_user_prompt(constructed_prompt)
    print(python_code)
    result = DockerFunctions.run_code_in_docker(python_code)
    
    print("\nResults based on GPT-4 generated code:")
    print(result["info"])
    print(result["status"])
    print(result["code"])
