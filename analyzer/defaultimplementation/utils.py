import re

from grammar.model.Grammar import Grammar
from grammar.model.RuleBodyElement import RuleBodyElementType
from logger.GlobalLogger import GlobalLogger

brackets_pairs = 'brackets_pairs'
instructions_seps = 'instructions_seps'


def get_prefix(code: str, target: str):
    if code.__contains__(target):
        return code[:code.find(target)]
    else:
        return code


def get_suffix(code: str, target: str):
    if code.__contains__(target):
        return code[code.find(target) + len(target):]
    else:
        return code


def get_first_term(body_items: list):
    for item in body_items:
        if RuleBodyElementType.VALUE == item.element_type:
            return item

    return None


def get_balanced_sub_sequence(grammar: Grammar, code: str, target: str):
    target_str = code
    for body in grammar.get_rules()[instructions_seps].get_bodies():
        for item in body.get_elements():
            tmp_str = get_prefix(code, item.string)
            if len(tmp_str) < len(target_str):
                target_str = tmp_str

    if re.search(target, target_str) is None:
        return ['', code]

    opening = []
    closing = []
    close_to_open = {}

    try:
        for body in grammar.get_rules()[brackets_pairs].get_bodies():
            items = body.get_elements()
            opening.append(items[0].string)
            closing.append(items[1].string)
            close_to_open[items[1].string] = items[0].string
    except Exception as e:
        GlobalLogger.log_error(e)
        return ['', code]

    r_prefix = '^\\s*'

    stack = []
    end_pos = -1

    for i in range(0, len(target_str)):
        cur_str = target_str[i:]

        if cur_str[0] == ' ':
            continue

        match_target = re.match(r_prefix + target, cur_str)
        if match_target is not None:
            if len(stack) == 0:
                end_pos = i
                break

        for o in opening:
            match = re.match(r_prefix + o, cur_str)
            if match is not None:
                stack.append(str(o))
                break

        for c in closing:
            match = re.match(r_prefix + c, cur_str)
            if match is not None:
                if len(stack) > 0 and stack[-1] == close_to_open[c]:
                    stack.pop()
                else:
                    return ['', code]

    if end_pos == -1:
        return ['', code]
    else:
        return [target_str[:end_pos], target_str[end_pos:] + get_suffix(code, target_str)]
