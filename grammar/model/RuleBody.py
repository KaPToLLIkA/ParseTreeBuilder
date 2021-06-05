from grammar.model import RuleBodyElement


class RuleBody:
    def __init__(self):
        self._elements = []

    def add_element(self, element: RuleBodyElement):
        self._elements.append(element)

    def get_elements(self):
        return self._elements
