import codecs

from grammar.interfaces.IGrammarLoader import IGrammarLoader


characters_black_list = '\n\t\b\r\f\v\a'


class GrammarLoader(IGrammarLoader):
    def __init__(self):
        self.raw_grammar = ""

    def load_from_file(self, file_name: str):
        self.raw_grammar = ""
        in_file = codecs.open(file_name, 'r', 'utf-8')

        for line in in_file:
            _line = line

            for character in characters_black_list:
                _line = str(_line).replace(character, '')

            if _line and _line[0] != '#':
                self.raw_grammar += _line

        in_file.close()
