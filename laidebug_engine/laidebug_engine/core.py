import bdb
import ast
from .llm import LLMWrapper
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
    def __init__(self, file_content, function_name):
        super().__init__()
        self.file_content = file_content
        self.source_lines = self.file_content.splitlines()
        self.function_name = function_name
        self.execution_information = FunctionExecutionInformation(function_name, None)

    def execute(self):
        self.run(f"exec('''{self.file_content}''')")
        self.execution_information.function_content = self.get_function_source()

    def user_line(self, frame):
        if frame.f_code.co_name == self.function_name:
            line_content = self.source_lines[frame.f_lineno - 1]
            line_info = LineExecutionInformation(frame.f_lineno, line_content, deepcopy(frame.f_locals))
            self.execution_information.add_line_execution(line_info)

    def get_function_source(self):
        tree = ast.parse(self.file_content)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == self.function_name:
                start_line = node.lineno - 1
                end_line = max(getattr(node, "end_lineno", start_line + 1), start_line + 1)
                return "\n".join(self.file_content.splitlines()[start_line:end_line])


def convert_to_prompt(func_exec_info):
    if not func_exec_info.line_executions:
        return None

    messages = []
    messages.append(
        f"Your task is to analyze function '{func_exec_info.function_name}' and report any unexpected behaviour."
    )

    for line in func_exec_info.line_executions:
        messages.append(f"-> Local variables currently are:")
        messages.append("\n".join(f"'{var}': {val}" for var, val in line.local_variables.items()))
        messages.append(f"-> Line {line.line_no} will be executed.")
        messages.append(f"-> Line content is:\n{line.line_content.rstrip()}")

    messages.append("The function has ended.")
    messages.insert(
        1, f"The full function consists of the given lines of code:\n{func_exec_info.function_content}"
    )

    return "\n".join(messages)


def debug_function(file_content, function_name, model_name, api_key):
    debugger = LaiDebugger(file_content, function_name)
    debugger.execute()
    model = LLMWrapper(model_name, api_key)
    prompt = convert_to_prompt(debugger.execution_information)
    if prompt is None:
        raise Exception(
            f"Breakpoint was not hit at given function '{function_name}'. No prompt could be generated."
        )

    print(prompt)
    return model.ask(prompt)
