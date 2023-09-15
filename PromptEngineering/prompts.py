class Prompts:
    
    @staticmethod
    def function(user_input: str, language: str = 'python') -> str:
        template = (
            f"Write a {language.capitalize()} function based on the following specifications:\n\n"
            f"- Function requirements:\n"
            f"  * Only import standard {language.capitalize()} libraries. Do not use local libraries or functions.\n"
            f"  * The function should be complete, standalone, and self-sufficient.\n"
            f"  * Avoid using object-oriented programming (OOP) if not idiomatic to {language}. Design the function in a procedural style.\n"
            f"  * Ensure proper validation, error handling, and clarity in the code. Follow proper naming conventions and provide necessary comments.\n"
            f"  * Avoid unconventional or 'hacky' solutions. If security considerations are relevant, address them in the function's logic.\n"
            f"  * Respect {language.capitalize()}'s best practices and conventions in coding.\n"
            f"  * Generate ONLY the requested function. Do not provide auxiliary functions, examples, or any extra code. The objective is to create a function that can be seamlessly integrated into an existing {language.capitalize()} application.\n"
            f"  * Write production-level code prioritising optimisation, efficiency, and security.\n"
            f"  * Think step by step in your approach and SHOW YOUR WORKING as comprehensive comments.\n"
            f"  * At the end, you must generate unit testing. Do not use external libraries; use mock data, multiple scenarios, descriptive messages, and handle edge cases.\n"
            f"  * Unit tests should be FULLY printed, described, clear, and interesting for the user.\n"
            f"  * Generated function must be called.\n"
            f"  * User interaction is not possible; user input/interaction MUST be simulated.\n"
            f"  * ALL DEFINED FUNCTIONS MUST BE CALLED.\n\n"
            f"  * ALL FAILED UNIT TESTS MUST RAISE ERRORS.\n"
            f"{user_input}"
        )
        return template

    @staticmethod
    def big_o(code: str, language: str = 'python') -> str:
        return (
            f"Given the following {language.capitalize()} code:\n\n"
            f"```{language}\n{code}\n```\n\n"
            f"Provide the Big O notation (time complexity) for the code.\n"
            f"ONLY PROVIDE THE NOTATION. NO EXPLAINATION, NO PLACEHOLDERS, NOTHING ELSE."
        )

    @staticmethod
    def fix_code(code: str, error_message: str, language: str = 'python') -> str:
        return (
            f"Given the following {language.capitalize()} code:\n\n"
            f"```{language}\n{code}\n```\n\n"
            f"The code produced the following error:\n"
            f"```{error_message}\n```\n\n"
            f"- Think methodically about the problem. Begin by understanding the expected functionality of the code.\n"
            f"- Consider potential pitfalls or common mistakes in the code structure, logic, or the use of {language.capitalize()} constructs.\n"
            f"- NEVER provide any installation commands in the output; I WILL handle this manually."
        )

    @staticmethod
    def describe_function(code: str, language: str = 'python') -> str:
        return (
            f"Given the function:\n\n"
            f"```{language}\n{code}\n```\n\n"
            f"Briefly describe its purpose, parameters, return values, and notable behaviors. Avoid verbosity. Should be Simple for A Beginner and around 50 words."
        )
    
    @staticmethod
    def package_install(code: str, language: str = 'python') -> str:
        return (
            f"Given the following {language.capitalize()} code:\n\n"
            f"```{language}\n{code}\n```\n\n"
            f"Please provide the EXACT package installation commands (e.g., for Python: 'pip install XYZ', for JavaScript: 'npm install XYZ', etc.) required for this code. No explanation, placeholders, or instructions; it should be directly executable. If no packages are required, ONLY return - []."
        )
    @staticmethod
    def execution_command(code: str) -> str:
        return (
            f"Given the following code:\n\n"
            f"```{code}\n```\n\n"
            f"Provide the EXACT command required to execute this code. No explanation, placeholders, or instructions; it should be directly executable. If no execution command is required, ONLY return - []."
        )
