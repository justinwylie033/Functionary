from Fixing.FixCode import FixCode
from Docker.DockerFunctions import DockerFunctions

docker = DockerFunctions()

def test_fix_functionality():
    test_cases = [
        {
            "code": """def matrix_chain_order(p):
                  n = len(p) - 1
                  m = [[0 for x in range(n)] for x in range(n)]
                  s = [[0 for x in range(n)] for x in range(n)]
                  for l in range(2, n):
                      for i in range(1, n-l+1):
                          j = i + l - 1
                          m[i][j] = float('inf')
                          for k in range(i, j):
                              q = m[i][k] + m[k+1][j] + p[i-1]*p[k]*p[j]
                              if q < m[i][j]:
                                  m[i][j] = q
                                  s[i][j] = k
                  return m, s

              p = [30, 35, 15, 5, 10, 20, 25]
              m, s = matrix_chain_order(p)
              print(m[1][len(p)-1])"""
        },
        # Syntax error
        {"code": "print('Hello World!'"},
        # Semantic error
        {"code": "print(x)"},
        # Runtime error
        {"code": "print(1/0)"},
        # Logical error
        {"code": "def add(a, b): return a-b\nprint(add(1, 2))"},
        # Non-Python code
        {"code": "console.log('Hello from JavaScript!');"},
        # Ambiguous Error
        {"code": "def greet():\n    print('Hello')\ngreett()"},
        # No Error
        {"code": "print('Hello')"}
        # More cases can be added...
    ]

    for idx, test in enumerate(test_cases, 1):
        print(f"Running test case {idx}...")

        current_code = test["code"]
        max_attempts = 5  # prevent infinite loops, by setting a max number of attempts
        attempts = 0

        while attempts < max_attempts:
            execution_result = docker.run_code_in_docker(current_code)
            print(execution_result)
            if execution_result["status"] == "success":
                print("Code executed successfully without errors.")
                break

            print("Executing code resulted in an error: retrying... ")
            print(execution_result["info"])

            fix_result = FixCode.fix_code(
                current_code, execution_result["info"])
            current_code = fix_result["corrected_code"]

            print(fix_result)

            # Print the fixed code to the terminal
            print("\n--- Fixed Code (Attempt {}) ---".format(attempts+1))
            print(current_code)
            print("-------------------\n")

            attempts += 1

        if execution_result["status"] == "success":
            print(f"Test case {idx} passed after {attempts} attempts!")
        else:
            print(
                f"Test case {idx} failed even after {max_attempts} attempts. Last Error: {execution_result['info']}")

if __name__ == "__main__":
    test_fix_functionality()
