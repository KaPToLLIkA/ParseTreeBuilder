import re

from analyzer.interfaces.ITokenizer import ITokenizer
from analyzer.model.Token import Token
from logger.GlobalLogger import GlobalLogger


class Tokenizer(ITokenizer):
    r_keywords = r'(abstract)|(assert)|(boolean)|(break)|(byte)|(case)|' \
                 r'(catch)|(char)|(class)|(const)|(continue)|(default)|' \
                 r'(do)|(double)|(else)|(final)|(finally)|(float)|(for)|' \
                 r'(goto)|(if)|(implements)|(import)|(instanceof)|(int)|' \
                 r'(interface)|(long)|(native)|(new)|(non-sealed)|(package)|' \
                 r'(protected)|(public)|(return)|(short)|(static)|(strictfp)|' \
                 r'(super)|(switch)|(synchronized)|(this)|(throw)|(throws)|' \
                 r'(transient)|(try)|(void)|(volatile)|(while)|(permits)|' \
                 r'(record)|(sealed)|(var)|(yield)|(const)'
    r_literals = r'([+-]?\d+\.?\d*)|(\"[^\"]*\")|(\'[^\']*\')'
    r_identifiers = r'[_a-zA-Z][_\-A-Za-z0-9]*'
    r_brackets = r'(\()|(\))|({)|(})|(\[)|(\])'
    r_operators = r'(\+)|(\-)|(\+=)|(\-=)|(\*=)|(/=)|(%=)|(\+\+)|(\-\-)|' \
                  r'(==)|(!=)|(<)|(<=)|(>)|(>=)|(!)|(&&)|(\|\|)|(&)|(\|)|' \
                  r'(\^)|(~)|(>>)|(<<<)|(<<)|(=)|(;)|(,)|(/)|(\*)|(%)'
    r_spaces = r'\s*'
    r_prefix = r'^'

    r = [r_spaces, r_keywords, r_operators, r_literals, r_identifiers, r_brackets]

    def __init__(self, code: str):
        self.code = code
        self.tokes = []

    def tokenize(self):
        cur_code = self.code
        self.tokes = []

        while cur_code:
            for pattern in Tokenizer.r:
                match = re.match(Tokenizer.r_prefix + pattern, cur_code)
                if match is not None:
                    string = str(match[0]).strip()
                    cur_code = cur_code[match.end():]
                    if string:
                        self.tokes.append(Token(string))
                        break
                else:
                    if pattern == Tokenizer.r[-1]:
                        GlobalLogger.log_error(f"Can't parse token at:{cur_code}")
                        return False
        return True

    def tokens_to_code(self):
        string = ''
        for t in self.tokes:
            string += f'{t.value}'

        return string

    def __str__(self):
        string = '\n'
        for t in self.tokes:
            string += f'Token [{self.tokes.index(t):5}]: {t.value}\n'

        return string
