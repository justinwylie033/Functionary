class Prompts:

    @staticmethod
    def function(user_input: str) -> str:
        template = (f"Write a Python function based on the following specifications:\n\n"
                    f"- Function requirements:\n"
                    f"  * Only import standard Python libraries. Do not use local libraries or functions.\n"
                    f"  * The function should be complete, standalone, and self-sufficient.\n"
                    f"  * Avoid using object-oriented programming (OOP). Design the function in a procedural style.\n"
                    f"  * Ensure proper validation, error handling, and clarity in the code. Follow proper naming conventions and provide necessary comments.\n"
                    f"  * Avoid unconventional or 'hacky' solutions. If security considerations are relevant, address them in the function's logic.\n"
                    f"  * Respect Python's best practices and conventions in coding.\n"
                    f"  * Generate ONLY the requested function. Do not provide auxiliary functions, examples, or any extra code. The objective is to create a function that can be seamlessly integrated into an existing Python application.\n"
                    f"  * Write production-level code prioritising optimisation, efficiency, and security.\n"
                    f"  * Think step by step in your approach and SHOW YOUR WORKING as comprehensive comments.\n"
                    f"  * At the end you must generate unit testing, do not use external libraries, use mock data, multiple scenarios, descriptive messages and handle edge cases\n"
                    f"  * Unit tests should be FULLY printed, described, clear and interesting for the user\n"
                    f"  * Generated function must be called.\n"
                    f"  * User interaction is not possible, user input/interaction MUST be simulated\n"
                    f"  * ALL DEFINED FUNCTIONS MUST BE CALLED\n\n"
                    f"  * ALL FAILED UNIT TESTS MUST RAISE ERRORS."
                    f"{user_input}")
        
        return template

    @staticmethod
    def big_o(code: str) -> str:
        return (f"Given the following Python code:\n\n"
                f"```python\n{code}\n```\n\n"
                f"Provide the Big O notation (time complexity) for the code.\n"
                f"ONLY PROVIDE THE NOTATION. NO EXPLAINATION, NO PLACEHOLDERS, NOTHING ELSE")

    @staticmethod
    def fix_code(code: str, error_message: str) -> str:
        return (f"Given the following Python code:\n\n"
                f"```python\n{code}\n```\n\n"
                f"The code produced the following error:\n"
                f"```{error_message}\n```\n\n"
                f"- Think methodically about the problem. Begin by understanding the expected functionality of the code.\n"
                f"- Consider potential pitfalls or common mistakes in the code structure, logic, or the use of Python constructs.\n"
                f"- Follow these steps to correct the code:\n"
                f"  1. Identify problematic areas or inefficiencies in the code.\n"
                f"  2. Address each of these areas, ensuring the code is optimized for performance.\n"
                f"  3. Validate that the solution adheres to Python best practices, avoiding unconventional or 'hacky' solutions.\n"
                f"  4. Provide necessary comments to explain each correction, ensuring clarity and maintainability.\n"
                f"- Once all corrections are made, provide the revised and correct version of the code.\n"
                f"- NEVER provide any installation commands in the output, I WILL handle this manually. ")
    
    @staticmethod
    def describe_function(code: str) -> str:
        return (f"Given the function:\n\n"
                f"```python\n{code}\n```\n\n"
                f"Briefly describe its purpose, parameters, return values, and notable behaviors. Avoid verbosity. Should be Simple for A Beginner and around 50 words")

    
    @staticmethod
    def package_install(code: str) -> str:
        """
        Generates a prompt to determine which packages need to be installed for the given code.

        Parameters:
        - code (str): The Python code to check for external dependencies.

        Returns:
        - str: A prompt asking the AI to list required package installation commands.
        """
        return (f"Given the following Python code:\n\n"
                f"```python\n{code}\n```\n\n"
                f"Please provide the EXACT package installation commands (e.g., 'pip install XYZ') required for this code, and NOTHING ELSE. no explanation, placeholders, instructions, should be directly executable"
                f"if no packages required ONLY return - []")
