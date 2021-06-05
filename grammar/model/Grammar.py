from grammar.model import Rule


class Grammar:
    def __init__(self):
        self._rules = {}

    def add_rule(self, rule: Rule):
        self._rules[rule.head] = rule

    def get_rules(self):
        return self._rules
