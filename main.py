from Fixing.FixCode import FixCode
from Docker.DockerFunctions import DockerFunctions
from Generation.generate_code import CodeGeneration
from Analysis.AnalyseCode import CodeAnalyser
from Installation.install_packages import install_packages
from DB.db import FunctionaryDB


def execute_and_fix(python_code: str, max_attempts: int = 5):
    for attempt in range(max_attempts):
        print("Installing Packages if necessary...")
        install_packages(python_code)
        
        execution_result = DockerFunctions.run_python_in_docker(python_code)
        
        if execution_result["status"] == "success":
            return "success", execution_result["info"], python_code

        print(f"\nError on attempt {attempt + 1}:\n{execution_result['info']}")
        print("\n Attempting Fix Please Wait...")

        fix_result = FixCode.fix_code(python_code, execution_result["info"])
        python_code = fix_result["corrected_code"]
        print("\nGenerated Fix:\n", python_code)

    return execution_result["status"], execution_result["info"], python_code

def generate_and_test_code(initial_prompt: str):
    print("\nGenerating code based on your requirement...")
    current_prompt = CodeGeneration.generate_function_prompt(initial_prompt)
    python_code = CodeGeneration.generate_code(current_prompt)
    print("\nGenerated Code:\n", python_code)
    
    status, info, final_code = execute_and_fix(python_code)
    efficiency = CodeAnalyser.get_big_o_notation(final_code)
    
    return {
        "info": info,
        "status": status,
        "code": final_code,
        "efficiency": efficiency
    }

if __name__ == "__main__":
    # Initial Docker testing
    print("Initial testing with Docker...")
    python_code = "print('Hello from Docker!')"
    docker_test_result = DockerFunctions.run_python_in_docker(python_code)
    
    if docker_test_result["status"] != "success":
        print("Error initializing Docker. Please ensure Docker is running correctly.")
        exit()

    print("Docker initialization successful.\n")

    # Initialize the FunctionaryDB
    db = FunctionaryDB()

    # User input for code generation
    initial_prompt = input("Please describe the function you want GPT-4 to generate: ")

    # Check if the function with the given requirements already exists in the database
    existing_functions = db.query_data(code=initial_prompt)
    if existing_functions:
        print("\nFunction already exists in our database!")
        for func in existing_functions:
            code, efficiency, output = func
            print("\nCode:\n", code)
            print("Efficiency:", efficiency)
            print("Output:", output)
        exit()

    # If function doesn't exist, generate, test, and fix it
    result = generate_and_test_code(initial_prompt)

    # Upsert the function into the database
    print("Adding the function to the functionary ")
    db.upsert_functions(result["code"], result["efficiency"], result["info"])

    print("\nFinal Results:")
    print("----------------")
    print("Info:", result["info"])
    print("Execution Status:", result["status"])
    print("Final Code:\n", result["code"])
    print("Code Efficiency:", result["efficiency"])

