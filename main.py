from analyzer.defaultimplementation.CodeLoader import CodeLoader
from analyzer.java.ParseTreeBuilder import ParseTreeBuilder
from analyzer.java.Tokenizer import Tokenizer
from grammar.defaultimplementation.GrammarAnalyzer import GrammarAnalyzer
from grammar.defaultimplementation.GrammarLoader import GrammarLoader
from logger.GlobalLogger import GlobalLogger

file_with_grammar = 'java_context_free_grammar.grm'
file_with_code = './codeexamples/input.java'

if __name__ == '__main__':
    # grammar_loader = GrammarLoader()
    # grammar_loader.load_from_file(file_with_grammar)
    #
    # grammar_analyzer = GrammarAnalyzer()
    # grammar_analyzer.analyze(grammar_loader.raw_grammar)
    #
    # GlobalLogger.log_info('Grammar description:')
    # GlobalLogger.log_info(grammar_analyzer.grammar)
    # GlobalLogger.log_info('End of grammar description.')

    code_loader = CodeLoader(file_with_code)
    code_loader.load()

    GlobalLogger.log_info(f'Code from "{file_with_code}":')
    GlobalLogger.log_info(code_loader.code)
    GlobalLogger.log_info('End of code.')

    code_tokenizer = Tokenizer(code_loader.code)
    code_tokenizer.tokenize()

    GlobalLogger.log_info(f'Tokens from code:')
    GlobalLogger.log_info(code_tokenizer)
    GlobalLogger.log_info('End of tokens.')

    GlobalLogger.log_info(f'Code from tokens:')
    GlobalLogger.log_info(code_tokenizer.tokens_to_code())
    GlobalLogger.log_info('End of code.')

    tree_builder = ParseTreeBuilder(code_tokenizer.tokes)
    tree_builder.build_tree()
    GlobalLogger.log_info(tree_builder.__str__())
