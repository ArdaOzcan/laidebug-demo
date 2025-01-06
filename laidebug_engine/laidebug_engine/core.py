import bdb
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
        self.function_name = function_name
        self.execution_information = FunctionExecutionInformation(function_name, self.get_function_source())

    def execute(self):
        self.run(f'exec("""{self.file_content}""")')

    def user_line(self, frame):
        # Only step through the specified function
        if frame.f_code.co_name == self.function_name:
            line_content = self.get_source_line(frame)
            line_info = LineExecutionInformation(frame.f_lineno, line_content, deepcopy(frame.f_locals))
            self.execution_information.add_line_execution(line_info)

        super().user_line(frame)

    def get_source_line(self, frame):
        lines = self.file_content.split("\n")
        return lines[frame.f_lineno - 1]

    def get_function_source(self):
        lines = self.file_content.split("\n")
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

        return "".join(function_source[:-trailing_whitespace])


def convert_to_prompt(func_exec_info):
    if not func_exec_info.line_executions:
        return None

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


def debug_function(file_content, function_name, model_name, api_key):
    debugger = LaiDebugger(file_content, function_name)
    debugger.execute()
    model = LLMWrapper(model_name, api_key)
    prompt = convert_to_prompt(debugger.execution_information)
    if prompt is None:
        raise Exception(
            f"Breakpoint was not hit at given function '{function_name}'. No prompt could be generated."
        )

    return model.ask(prompt)
