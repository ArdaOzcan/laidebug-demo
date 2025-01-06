import argparse
from .core import debug_function
from .llm import LLMWrapper

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Debug a Python script with a breakpoint at a specific function."
    )
    parser.add_argument("file_path", type=str, help="Path to the Python script to debug.")
    parser.add_argument("function_name", type=str, help="Name of the function to set a breakpoint.")
    parser.add_argument("model_name", type=str, help="Name of the llm model to use")
    parser.add_argument("api_key", type=str, help="API key for the llm model to use")

    args = parser.parse_args()

    with open(args.file_path, "r") as file:
        response = debug_function(file.read(), args.function_name, args.model_name, args.api_key)
        print(response)
