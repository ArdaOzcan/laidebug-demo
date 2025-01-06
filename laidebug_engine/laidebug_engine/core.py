import bdb
import argparse
from copy import deepcopy


class LineExecutionInformation:
    def __init__(self, line_no, line_content, local_variables):
        self.line_no = line_no
        self.line_content = line_content
        self.local_variables = local_variables


class FunctionExecutionInformation:
    def __init__(self, function_name, function_content):
        self.function_name = function_name
        self.function_content = function_content
        self.line_executions = []

    def add_line_execution(self, line_execution):
        self.line_executions.append(line_execution)


class LaiDebugger(bdb.Bdb):
    def __init__(self, filename, function_name):
        super().__init__()
        self.filename = filename
        self.function_name = function_name
        self.execution_information = FunctionExecutionInformation(function_name, self.get_function_source())

    def execute(self):
        self.run(f'exec(open("{self.filename}").read())')

    def user_line(self, frame):
        # Only step through the specified function
        if frame.f_code.co_name == self.function_name:
            line_content = self.get_source_line(frame)
            line_info = LineExecutionInformation(frame.f_lineno, line_content, deepcopy(frame.f_locals))
            self.execution_information.add_line_execution(line_info)

        super().user_line(frame)

    def get_source_line(self, frame):
        with open(self.filename, "r") as file:
            lines = file.readlines()
            return lines[frame.f_lineno - 1]

    def get_function_source(self):
        with open(self.filename, "r") as file:
            lines = file.readlines()
            function_source = []
            inside_function = False
            trailing_whitespace = 0
            for i, line in enumerate(lines):
                if line.lstrip().startswith(f"def {self.function_name}"):
                    inside_function = True
                elif line != "\n" and not line.startswith(" "):
                    break

                if inside_function:
                    if line.strip() == "":
                        trailing_whitespace += 1
                    else:
                        trailing_whitespace = 0
                    function_source.append(f"line {i+1}:{line}")

            for i, line in enumerate(reversed(function_source)):
                if line.strip() != "":
                    break
                else:
                    function_source.pop(len(function_source) - i)

            return "".join(function_source[:-trailing_whitespace])


def convert_to_prompt(func_exec_info):
    messages = [
        f"Your task is to analyze function '{func_exec_info.function_name}' and report any unexpected behaviour."
    ]

    messages.append(
        f"The full function consists of the given lines of code:\n{func_exec_info.function_content}"
    )

    for line in func_exec_info.line_executions:
        messages.append(f"-> Local variables currently are:")
        messages.append("\n".join(f"'{var}': {val}" for var, val in line.local_variables.items()))
        messages.append(f"-> Line {line.line_no} will be executed.")
        messages.append(f"-> Line content is:\n{line.line_content.rstrip()}")

    messages.append("The function has ended.")

    return "\n".join(messages)
