import re

from analyzer.interfaces.IParseTreeBuilder import IParseTreeBuilder
from analyzer.model.TreeNode import TreeNode
from logger.GlobalLogger import GlobalLogger

class R:
    curly_o_br = r'\{'
    curly_c_br = r'\}'
    circle_o_br = r'\('
    circle_c_br = r'\)'
    square_o_br = r'['
    square_c_br = r']'

    literal = r'([+-]?\d+\.?\d*)|(\"[^\"]*\")|(\'[^\']*\')'
    identifier = r'[_a-zA-Z][_\-A-Za-z0-9]*'
    open_br = [circle_o_br, square_o_br, curly_o_br]
    close_br = [circle_c_br, square_c_br, curly_c_br]
    open_to_close_br = {circle_o_br: circle_c_br, curly_o_br: curly_c_br, square_o_br: square_c_br}

    field_of_view = r'(default)|(public)|(protected)|(private)'
    type_modifiers = r'final'
    static_modifier = r'static'

    types = r'(byte)|(short)|(int)|(long)|(float)|(double)|(char)|(boolean)|(void)'

    ops1 = r'(=)|(\+=)|(\-=)|(/=)|(%=)|(\*=)'

    instructions_sep = r';'


def str_cmp(pattern, target):
    return re.match(pattern, target.value) is not None


class RetVal:
    def __init__(self, flag, last_used_pos=-1):
        self.last_used_pos = last_used_pos
        self.flag = flag


class ParseTreeBuilder(IParseTreeBuilder):
    def __init__(self, tokens):
        self.tokens = tokens
        self.root = None

    def code_fragment(self, start: int, end: int):
        return ' '.join(map(lambda i: i.value, self.tokens[start:end]))

    def error_msg(self, msg: str, start: int, end: int):
        GlobalLogger.log_error(f'{msg} code: {self.code_fragment(start, end)}')

    def get_close_bracket(self, open_br, start: int, end: int):
        close_br = R.open_to_close_br[open_br]
        balance = 0
        br_index = start + end
        for i in range(start, end):
            if str_cmp(open_br, self.tokens[i]):
                balance += 1
            elif str_cmp(close_br, self.tokens[i]):
                balance -= 1
                if balance == 0:
                    br_index = i
                    break
        return br_index

    def _main(self, start: int, end: int, current_node: TreeNode):
        current_node.add_child(TreeNode('class_definitions'))
        rv = self._class_definitions(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
            return RetVal(False)
        return RetVal(True)

    def _field_of_view(self, start: int, end: int, current_node: TreeNode):
        if start >= end:
            return RetVal(False)
        if str_cmp(R.field_of_view, self.tokens[start]):
            current_node.add_child(TreeNode(self.tokens[start]))
            return RetVal(True)
        else:
            current_node.add_child(TreeNode(''))
            return RetVal(False)

    def _type_modifiers(self, start: int, end: int, current_node: TreeNode):
        if start >= end:
            return RetVal(False)
        if str_cmp(R.type_modifiers, self.tokens[start]):
            current_node.add_child(TreeNode(self.tokens[start]))
            return RetVal(True)
        else:
            current_node.add_child(TreeNode(''))
            return RetVal(False)

    def _static_modifier(self, start: int, end: int, current_node: TreeNode):
        if start >= end:
            return RetVal(False)
        if str_cmp(R.static_modifier, self.tokens[start]):
            current_node.add_child(TreeNode(self.tokens[start]))
            return RetVal(True)
        else:
            current_node.add_child(TreeNode(''))
            return RetVal(False)

    def _types(self, start: int, end: int, current_node: TreeNode):
        if start >= end:
            return RetVal(False)
        if str_cmp(R.types, self.tokens[start]):
            current_node.add_child(TreeNode(self.tokens[start]))
        else:
            self.error_msg('Where is type?', start, end)
            return RetVal(False)
        return RetVal(True, start)

    def _identifier(self, start: int, end: int, current_node: TreeNode):
        if start >= end:
            return RetVal(False)
        if str_cmp(R.identifier, self.tokens[start]):
            current_node.add_child(TreeNode(self.tokens[start]))
        else:
            self.error_msg('Where is identifier?', start, end)
            return RetVal(False)
        return RetVal(True, start)

    def _class_name(self, start: int, end: int, current_node: TreeNode):
        if start >= end:
            return RetVal(False)
        if str_cmp(R.identifier, self.tokens[start]):
            current_node.add_child(TreeNode(self.tokens[start]))
        else:
            self.error_msg('Where is class name?', start, end)
            return RetVal(False)
        return RetVal(True, start)

    def _class_definitions(self, start: int, end: int, current_node: TreeNode):
        if start >= end:
            return RetVal(False)

        current_node.add_child(TreeNode('field_of_view'))
        rv = self._field_of_view(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
        else:
            start += 1

        if str_cmp('class', self.tokens[start]):
            current_node.add_child(TreeNode(self.tokens[start]))
        else:
            self.error_msg('Where is "class" keyword?', start, end)
            return RetVal(False)

        start += 1
        current_node.add_child(TreeNode('class_name'))
        rv = self._class_name(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
            return RetVal(False)

        start += 1
        if str_cmp(R.curly_o_br, self.tokens[start]):
            current_node.add_child(TreeNode(self.tokens[start]))
            new_end = self.get_close_bracket(R.curly_o_br, start, end)
            if new_end < end:
                current_node.add_child(TreeNode('class_body'))
                rv = self._class_body(start + 1, new_end, current_node.get_last_child())
                if not rv.flag:
                    current_node.remove_last()
                    return RetVal(False)
                new_end += 1
                if str_cmp(R.instructions_sep, self.tokens[new_end]):
                    current_node.add_child(TreeNode(self.tokens[new_end]))
                    current_node.add_child(TreeNode('class_definitions'))
                    new_end += 1
                    rv = self._class_definitions(new_end, end, current_node.get_last_child())
                    if not rv.flag:
                        current_node.remove_last()
                        new_end -= 1
                    else:
                        new_end = rv.last_used_pos
                else:
                    self.error_msg('Where is instructions separator?', new_end, end)
                    return RetVal(False)
            else:
                self.error_msg('Where is close curly bracket?', start, end)
                return RetVal(False)
        else:
            self.error_msg('Where is curly bracket?', start, end)
            return RetVal(False)
        return RetVal(True, new_end)

    def _class_body(self, start: int, end: int, current_node: TreeNode):
        current_node.add_child(TreeNode('definitions'))
        rv = self._definitions(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
            return RetVal(False)
        return RetVal(True)

    def _definitions(self, start: int, end: int, current_node: TreeNode):
        if start >= end:
            return RetVal(False, start)

        current_node.add_child(TreeNode('class_definitions'))
        rv = self._class_definitions(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
        else:
            start = rv.last_used_pos + 1

        current_node.add_child(TreeNode('field_def'))
        rv = self._field_def(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
        else:
            start = rv.last_used_pos + 1

        current_node.add_child(TreeNode('method_def'))
        rv = self._method_def(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
        else:
            start = rv.last_used_pos + 1

        current_node.add_child(TreeNode('definitions'))
        rv = self._definitions(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
        else:
            start = rv.last_used_pos

        return RetVal(True, start)

    def _field_def(self, start: int, end: int, current_node: TreeNode):
        if start >= end:
            return RetVal(False)

        current_node.add_child(TreeNode('field_of_view'))
        rv = self._field_of_view(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()

        start += 1
        current_node.add_child(TreeNode('static_modifier'))
        rv = self._static_modifier(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
            start -= 1

        start += 1
        current_node.add_child(TreeNode('type_modifier'))
        rv = self._type_modifiers(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
            start -= 1

        start += 1
        current_node.add_child(TreeNode('types'))
        rv = self._types(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
            return RetVal(False)

        start += 1
        current_node.add_child(TreeNode('identifier'))
        rv = self._identifier(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
            return RetVal(False)

        start += 1
        if str_cmp(R.instructions_sep, self.tokens[start]):
            current_node.add_child(TreeNode(self.tokens[start]))
        else:
            if str_cmp('=', self.tokens[start]) \
                    and str_cmp(R.literal, self.tokens[start + 1])\
                    and str_cmp(R.instructions_sep, self.tokens[start + 2]):
                current_node.add_child(TreeNode(self.tokens[start]))
                current_node.add_child(TreeNode(self.tokens[start+1]))
                current_node.add_child(TreeNode(self.tokens[start+2]))
                start += 2
            else:
                return RetVal(False)
        return RetVal(True, start)

    def _method_def(self, start: int, end: int, current_node: TreeNode):
        if start >= end:
            return RetVal(False)

        current_node.add_child(TreeNode('field_of_view'))
        rv = self._field_of_view(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()

        start += 1
        current_node.add_child(TreeNode('static_modifier'))
        rv = self._static_modifier(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
            start -= 1

        start += 1
        current_node.add_child(TreeNode('type_modifier'))
        rv = self._type_modifiers(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
            start -= 1

        start += 1
        current_node.add_child(TreeNode('types'))
        rv = self._types(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
            return RetVal(False)

        start += 1
        current_node.add_child(TreeNode('identifier'))
        rv = self._identifier(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
            return RetVal(False)

        start += 1
        if str_cmp(R.circle_o_br, self.tokens[start]):
            new_end = self.get_close_bracket(R.circle_o_br, start, end)
            if new_end < end:
                current_node.add_child(TreeNode(self.tokens[start]))
                current_node.add_child(TreeNode('args_def'))
                self._args_def(start + 1, new_end, current_node.get_last_child())
                current_node.add_child(TreeNode(self.tokens[new_end]))

                new_end += 1
                start = new_end
                if str_cmp(R.curly_o_br, self.tokens[start]):
                    new_end = self.get_close_bracket(R.curly_o_br, start, end)
                    if new_end < end:
                        current_node.add_child(TreeNode(self.tokens[start]))
                        current_node.add_child(TreeNode('instructions'))
                        current_node.add_child(TreeNode(self.tokens[new_end]))
                        self._instructions(start + 1, new_end, current_node.get_last_child())

                        start = new_end
                    else:
                        return RetVal(False)
            else:
                return RetVal(False)
        else:
            return RetVal(False)

        return RetVal(True, start)

    def _args_def(self, start: int, end: int, current_node: TreeNode):
        if start >= end:
            return RetVal(False)

        current_node.add_child(TreeNode('type_modifier'))
        rv = self._type_modifiers(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
            start -= 1

        start += 1
        current_node.add_child(TreeNode('types'))
        rv = self._types(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
            return RetVal(False)

        start += 1
        current_node.add_child(TreeNode('identifier'))
        rv = self._identifier(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
            return RetVal(False)

        start += 1
        if str_cmp(',', self.tokens[start]):
            current_node.add_child(TreeNode(self.tokens[start].value))
            self._args_def(start + 1, end, current_node.get_last_child())

        return RetVal(True)

    def _instructions(self, start: int, end: int, current_node: TreeNode):
        if start >= end:
            return RetVal(False)

        current_node.add_child(TreeNode('expression'))
        rv = self._expression(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
        else:
            start = rv.last_used_pos + 1

        current_node.add_child(TreeNode('control'))
        rv = self._control(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
        else:
            start = rv.last_used_pos + 1

        if str_cmp(R.curly_o_br, self.tokens[start]):
            new_end = self.get_close_bracket(R.curly_o_br, start, end)
            current_node.add_child(TreeNode('{'))
            current_node.add_child(TreeNode('instructions'))
            rv = self._instructions(start + 1, new_end, current_node.get_last_child())
            if not rv.flag:
                current_node.remove_last()
                current_node.remove_last()
            else:
                start = new_end + 1
                current_node.add_child(TreeNode('}'))

        current_node.add_child(TreeNode('instructions'))
        rv = self._instructions(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
        else:
            start = rv.last_used_pos

        return RetVal(True, start)

    def _expression(self, start: int, end: int, current_node: TreeNode):
        if start >= end:
            return RetVal(False)

        current_node.add_child(TreeNode('types'))
        rv = self._types(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
        else:
            start += 1

        current_node.add_child(TreeNode('identifier'))
        rv = self._identifier(start, end, current_node.get_last_child())
        if not rv.flag:
            current_node.remove_last()
            return RetVal(False)

        start += 1
        if str_cmp(R.ops1, self.tokens[start]):
            current_node.add_child(TreeNode(self.tokens[start]))
            start += 1
            if str_cmp(R.literal, self.tokens[start]):
                current_node.add_child(TreeNode(self.tokens[start]))
            else:
                current_node.add_child(TreeNode('identifier'))
                rv = self._identifier(start, end, current_node.get_last_child())
                if not rv.flag:
                    current_node.remove_last()
                    return RetVal(False)
            start += 1
            if str_cmp(R.instructions_sep, self.tokens[start]):
                current_node.add_child(TreeNode(self.tokens[start]))
            else:
                return RetVal(False)
        else:
            return RetVal(False)

        return RetVal(True, start)

    def _control(self, start: int, end: int, current_node: TreeNode):
        return RetVal(False)

    def _math_expr(self, start: int, end: int, current_node: TreeNode):
        return RetVal(False)

    def build_tree(self):
        self.root = TreeNode('main')
        self._main(0, len(self.tokens), self.root)

    def _rec_to_str(self, cur_node: TreeNode, levels: list, d: int, le: int):
        for i in range(0, d):
            if i != d - 1:
                if levels[i]:
                    self._str += '|'
                else:
                    self._str += ' '
                for x in range(0, le):
                    self._str += ' '
            else:
                self._str += '+'

        if d > 0:
            for i in range(0, le):
                self._str += '-'

        self._str += cur_node.node_value.__str__() + '\n'

        levels.append(True)
        c = cur_node.get_child_s()
        for i in range(0, len(c)):
            if i == len(c) - 1:
                levels[-1] = False
            self._rec_to_str(c[i], levels, d + 1, le)
        levels.pop()

    def __str__(self):
        self._str = '\n'
        self._rec_to_str(self.root, [], 0, 4)
        return self._str
