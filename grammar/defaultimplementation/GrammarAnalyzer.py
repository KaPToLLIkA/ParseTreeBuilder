from grammar.interfaces.IGrammarAnalyzer import IGrammarAnalyzer
from grammar.model.Grammar import Grammar
from grammar.model.Rule import Rule
from grammar.model.RuleBody import RuleBody
from grammar.model.RuleBodyElement import RuleBodyElement, RuleBodyElementType
from logger.GlobalLogger import GlobalLogger


class GrammarAnalyzer(IGrammarAnalyzer):
    def __init__(self):
        self.grammar = Grammar()

    @staticmethod
    def _parse_rule(raw_rule):
        try:
            head, raw_bodies = list(map(lambda i: str(i).strip(), (str(raw_rule).split('->'))))

            bodies = list(map(lambda i: str(i).strip(), (str(raw_bodies).split(' |'))))

            rule = Rule(head)

            for raw_body in bodies:
                new_body = RuleBody()
                body_items = list(map(lambda i: str(i).strip(), (str(raw_body).split(' '))))

                for raw_body_item in body_items:
                    if raw_body_item.startswith('\"') and raw_body_item.endswith('\"'):
                        new_body.add_element(RuleBodyElement(raw_body_item[1:-1], RuleBodyElementType.VALUE))
                    elif raw_body_item.startswith('\"') or raw_body_item.endswith('\"'):
                        raise Exception('There are no closing or opening quotation marks')
                    else:
                        new_body.add_element(RuleBodyElement(raw_body_item, RuleBodyElementType.NEXT_RULE))

                rule.add_body(new_body)

        except Exception as e:
            GlobalLogger.log_error(f'Rule: "{raw_rule}" Error: "{e}"')
            rule = Rule('parsing_failed_no_use_it')
        return rule

    def analyze(self, raw_grammar):
        GlobalLogger.log_info('Start grammar analyze')
        rules_not_filtered = list(map(lambda i: str(i).strip(), (str(raw_grammar).split('end_def'))))
        rules = list(filter(lambda i: bool(i), rules_not_filtered))

        for rule_def in rules:
            GlobalLogger.log_info(rule_def)
            self.grammar.add_rule(self._parse_rule(rule_def))

        GlobalLogger.log_info('End grammar analyze')
