import google.generativeai as genai

SUPPORTED_MODELS = {"gemini-1.5-flash"}


class LLMWrapper:
    def __init__(self, model_name, api_key):
        if model_name not in SUPPORTED_MODELS:
            raise Exception(f"Model '{model_name}' is not supported")
        self.model_name = model_name
        self.api_key = api_key

    def ask(self, prompt):
        if self.model_name == "gemini-1.5-flash":
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return response.text
