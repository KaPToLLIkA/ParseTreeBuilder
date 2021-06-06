import codecs

from analyzer.interfaces.ICodeLoader import ICodeLoader


characters_black_list = '\n\t\b\r\f\v\a'


class CodeLoader(ICodeLoader):
    def __init__(self, f_name):
        self.f_name = f_name
        self.code = ''

    def load(self):
        self.code = ''
        in_file = codecs.open(self.f_name, 'r', 'utf-8')

        for line in in_file:
            _line = line

            for character in characters_black_list:
                _line = str(_line).replace(character, '')

            if _line:
                self.code += _line

        in_file.close()
