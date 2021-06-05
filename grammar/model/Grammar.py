from grammar.model import Rule


class Grammar:
    def __init__(self):
        self._rules = {}

    def add_rule(self, rule: Rule):
        self._rules[rule.head] = rule

    def get_rules(self):
        return self._rules

    def __str__(self):
        result_str = ''
        for key in self._rules:
            result_str += '\nRULE: {0}\n'.format(self._rules[key].head)

            for body in self._rules[key].get_bodies():
                result_str += '\tBODY:\n'

                for element in body.get_elements():
                    result_str += '\t\tELEMENT: {0:10} : {1}\n'\
                        .format(element.element_type.name, element.string)

        return result_str
