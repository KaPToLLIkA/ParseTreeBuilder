from grammar.model import RuleBody


class Rule:
    def __init__(self, head=""):
        self.head = head
        self._bodies = []

    def add_body(self, body: RuleBody):
        self._bodies.append(body)

    def get_bodies(self):
        return self._bodies
