from flask import Flask, request, jsonify
from DB.db import FunctionaryDB
from Generation.GenerateCode import CodeGeneration
from Analysis.AnalyseCode import CodeAnalyser
from Generation.DescribeFunction import DescribeFunction
from Docker.DockerFunctions import DockerFunctions
from Installation.install_packages import install_packages
from Fixing.FixCode import FixCode
from flask_cors import CORS
import logging
from decouple import config

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)
db = FunctionaryDB()
MAX_ATTEMPTS = int(config('MAX_ATTEMPTS'))


def install_required_packages(code: str):
    """Install required packages for the code."""
    logging.info("Installing Packages if necessary...")
    install_packages(code)


def execute_code_in_docker(code: str):
    """Execute python code in Docker and return the result."""
    return DockerFunctions.run_python_in_docker(code)


def fix_python_code(code: str, info: str):
    """Attempt to fix python code and return the corrected version."""
    logging.info("Attempting to fix the code...")
    return FixCode.fix_code(code, info)


@app.route('/generate-code', methods=['POST'])
def generate_code_endpoint():
    try:
        prompt = request.json.get('prompt')
        if not prompt:
            return jsonify({"error": "Prompt not provided"}), 400

        python_code = CodeGeneration.generate_code_from_user_prompt(prompt)
        efficiency = CodeAnalyser.get_big_o_notation(python_code)
    
        return jsonify({
            "code": python_code,
            "efficiency": efficiency
        })
    except Exception as e:
        # Log the error for debugging purposes
        logging.error(f"Error in generate_code_endpoint: {str(e)}")
        return jsonify({"error": "An unexpected error occurred."}), 500


@app.route('/execute-code', methods=['POST'])
def execute_code_endpoint():
    code = request.json.get('code')
    if not code:
        return jsonify({"error": "Code not provided"}), 400
    
    for _ in range(MAX_ATTEMPTS):
        result = execute_code_in_docker(code)
        if result["status"] == "success":
            description = DescribeFunction.generate_description_from_code(code)
            efficiency = CodeAnalyser.get_big_o_notation(code)
            db.upsert_functions(code, efficiency, result["info"], description)
            return jsonify({
                "info": result["info"],
                "status": result["status"],
                "efficiency": efficiency
            })
        else:
            # Attempt to fix the code
            corrected_code_response = fix_python_code(code, result["info"])
            if corrected_code_response.get('corrected_code'):
                code = corrected_code_response['corrected_code']
            else:
                # If no corrected code is returned, return an error
                return jsonify({"error": "Failed to fix the code after multiple attempts."}), 500

    return jsonify({"error": f"Failed to execute code successfully after {MAX_ATTEMPTS} attempts."}), 500




@app.route('/fix-code', methods=['POST'])
def fix_code_endpoint():
    print(request.json)  # Add this to see the incoming payload
    code = request.json.get('code')
    info = request.json.get('info')
    if not code or not info:
        return jsonify({"error": "Code or Error Info not provided"}), 400
    
    corrected_code = fix_python_code(code, info)
    return jsonify({"corrected_code": corrected_code})


@app.route('/install-packages', methods=['POST'])
def install_packages_endpoint():
    code = request.json.get('code')
    if not code:
        return jsonify({"error": "Code not provided"}), 400

    install_required_packages(code)
    return jsonify({"message": "Packages installation attempted!"})

@app.route('/describe-function', methods=['POST'])
def describe_function_endpoint():
    code = request.json.get('code')
    if not code:
        return jsonify({"error": "Code not provided"}), 400

    description = DescribeFunction.generate_description_from_code(code)
    return jsonify({"description": description})


@app.route('/search-code', methods=['GET'])
def search_code():
    query = request.args.get('query')
    results = db.search_code_by_description(query)  # Assuming you have such a method
    return jsonify({"results": results[:100] if results else "No results found"})



@app.route('/retrieve-code', methods=['POST'])
def retrieve_code_endpoint():
    criteria = {
        "code": request.json.get('code'),
        "efficiency": request.json.get('efficiency'),
        "output": request.json.get('output')
    }

    if not any(criteria.values()):
        return jsonify({"error": "Provide at least one search criterion (code/efficiency/output)"}), 400

    results = db.query_data(**criteria)
    return jsonify({"results": results[:100] if results else "No results found"})


if __name__ == '__main__':
    app.run(debug=True)
