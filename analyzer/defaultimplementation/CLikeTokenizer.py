import re

from analyzer.defaultimplementation.utils import get_balanced_sub_sequence, get_first_term
from analyzer.interfaces.ITokenizer import ITokenizer
from analyzer.model.Token import Token
from grammar.model.Grammar import Grammar
from grammar.model.Rule import Rule
from grammar.model.RuleBody import RuleBody
from grammar.model.RuleBodyElement import RuleBodyElementType
from logger.GlobalLogger import GlobalLogger

regexp_prefix = '^\\s*'


class CLikeTokenizer(ITokenizer):
    def __init__(self, grammar: Grammar, code: str):
        self.grammar = grammar
        self.tokens = []
        self.code = code

    def _rec_tokenize(self, next_rule_id, sub_code: str):
        ''':return [success, tokens, new_str]'''
        GlobalLogger.log_info(next_rule_id)
        GlobalLogger.log_info(sub_code)
        rule = self.grammar.get_rules()[next_rule_id]
        success = True
        tokens = []
        new_str = ''
        for body in rule.get_bodies():

            success = True
            new_str = sub_code
            tokens = []

            body_items = body.get_elements()
            for i in range(0, len(body_items)):
                if RuleBodyElementType.NEXT_RULE == body_items[i].element_type:

                    if i == 0 and body_items[i].string == next_rule_id:
                        term = get_first_term(body_items)
                        if term is None:
                            success = False
                            break

                        target, suffix = get_balanced_sub_sequence(self.grammar, new_str, term.string)

                        if target:
                            _success, _tokens, _new_str = self._rec_tokenize(body_items[i].string, target)

                            if _success:
                                tokens += _tokens
                                new_str = _new_str + suffix
                            else:
                                success = False
                                break
                        else:
                            success = False
                            break
                    else:
                        _success, _tokens, _new_str = self._rec_tokenize(body_items[i].string, new_str)

                        if _success:
                            tokens += _tokens
                            new_str = _new_str
                        else:
                            success = False
                            break

                elif RuleBodyElementType.VALUE == body_items[i].element_type:
                    match = re.match(regexp_prefix + body_items[i].string, new_str)

                    if match is not None:
                        if match[0]:
                            tokens.append(Token(str(match[0]).strip()))
                        new_str = new_str[match.end():]
                    else:
                        success = False
                        break

            if success:
                break

        return [success, tokens, new_str]

    def tokenize(self):
        success, tokens, new_code = self._rec_tokenize('main', self.code)
        if success:
            self.tokens = tokens
            self.code = new_code
        return success

    def __str__(self):
        _str = ''
        for token in self.tokens:
            _str += f'{token.value}\n'

        return _str
