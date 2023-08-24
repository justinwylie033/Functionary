from flask import Flask, request, jsonify
from DB.db import FunctionaryDB
from generate_code import CodeGeneration
from Docker.DockerFunctions import DockerFunctions
from install_packages import install_packages
from fix_code import FixCode
from flask_cors import CORS  # <-- Import CORS


app = Flask(__name__)
CORS(app)  # <-- Enable CORS for your app


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
    efficiency = CodeGeneration.get_big_o_notation(final_code)
    
    return {
        "info": info,
        "status": status,
        "code": final_code,
        "efficiency": efficiency
    }

db = FunctionaryDB()

@app.route('/generate-code', methods=['POST'])
def generate_code_endpoint():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({"error": "Prompt not provided"}), 400

    result = generate_and_test_code(prompt)

    # Add the generated code to the database
    db.upsert_functions(result["code"], result["efficiency"], result["info"])
    
    return jsonify(result)


@app.route('/retrieve-code', methods=['POST'])
def retrieve_code():
    code = request.json.get('code')
    efficiency = request.json.get('efficiency')
    output = request.json.get('output')
    
    if not (code or efficiency or output):
        return jsonify({"error": "Provide at least one search criterion (code/efficiency/output)"}), 400

    results = db.query_data(code=code, efficiency=efficiency, output=output)
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)

