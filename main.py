from analyzer.defaultimplementation.CodeLoader import CodeLoader
from grammar.defaultimplementation.GrammarAnalyzer import GrammarAnalyzer
from grammar.defaultimplementation.GrammarLoader import GrammarLoader
from logger.GlobalLogger import GlobalLogger

file_with_grammar = 'java_context_free_grammar.grm'
file_with_code = './codeexamples/input.java'

if __name__ == '__main__':
    grammar_loader = GrammarLoader()
    grammar_loader.load_from_file(file_with_grammar)

    grammar_analyzer = GrammarAnalyzer()
    grammar_analyzer.analyze(grammar_loader.raw_grammar)

    GlobalLogger.log_info('Grammar description:')
    GlobalLogger.log_info(grammar_analyzer.grammar)
    GlobalLogger.log_info('End of grammar description.')

    code_loader = CodeLoader(file_with_code)
    code_loader.load()

    GlobalLogger.log_info(f'Code from "{file_with_code}":')
    GlobalLogger.log_info(code_loader.code)
    GlobalLogger.log_info('End of code.')

