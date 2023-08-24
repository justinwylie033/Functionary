# test_code_generation.py

from generate_code import CodeGeneration
from Docker.DockerFunctions import DockerFunctions

if __name__ == "__main__":
    print("Initial testing with Docker...")
    python_code = "print('Hello from Docker!')"
    docker_test_result = DockerFunctions.run_python_in_docker(python_code)
    print(docker_test_result["info"])
    print(docker_test_result["status"])
    print(docker_test_result["code"])
    print(docker_test_result.get("efficiency", "Efficiency data not available."))

    initial_prompt = input("Enter your function requirements for GPT-4: ")
    current_prompt = CodeGeneration.generate_function_prompt(initial_prompt)
    python_code = CodeGeneration.generate_code(current_prompt)
    result = CodeGeneration.execute_code(python_code)
    efficiency = CodeGeneration.get_big_o_notation(python_code)
    result["efficiency"] = efficiency
    
    print("\nResults based on GPT-4 generated code:")
    print(result["info"])
    print(result["status"])
    print(result["code"])
    print(result["efficiency"])
