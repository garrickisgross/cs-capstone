from typing import List

class FormElement:
    name: str
    input_type: str
    help_text: str

    def __init__(self, name: str, input_type: str, help_text: str):
        self.name = name
        self.input_type = input_type
        self.help_text = help_text

class FormData:
    
    def __init__(self, elements: List[FormElement], url: str ):
        self.elements = elements
        self.url = url


