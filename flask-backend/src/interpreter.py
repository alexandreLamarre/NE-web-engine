import parser
import numpy as np
from math import*
import matplotlib.pyplot as matplot
import regex

class Interpreter():
    """ Abstract class for Interpreters"""
    def __init__(self, regex):
        self.regex = regex

    def match(self, in_str):
        matches = regex.finditer(self.regex, in_str)
        res = []
        for m in matches:
            res.append(m.group(0))
        return res


class FunctionInterpreter(Interpreter):
    def __init__(self):
        regex_str = "(([a-zA-Z]|[0-9])+\s*\({1}([a-zA-Z](\s*,\s*)*)+(\){1})\s*={1})\s*(\((([^=\(\)]*)|(?6))*\))"
        super().__init__(regex_str)

    def partial_match_name(self, in_str):
        regex_str = "(.)*\s*\({1}([a-zA-Z](\s*,\s*)*)+(\){1})(\s*={1})\s*(\((([^=\(\)]*)|(?6))*\))"
        matches = regex.finditer(regex_str, in_str)
        res = []
        for m in matches:
            res.append(m.group(0))
        return res

    def partial_match_variables(self, in_str):
        regex_str = "(([a-zA-Z]|[0-9])+\s*(\({1}(.)*\){1})\s*={1})\s*(\((([^=\(\)]*)|(?5))*\))"
        matches = regex.finditer(regex_str, in_str)
        res = []
        for m in matches:
            res.append(m.group(0))
        return res

    def partial_match_function(self, in_str):
        regex_str = "(([a-zA-Z]|[0-9])+\s*\({1}([a-zA-Z](\s*,\s*)*)+(\){1})\s*={1})(.)*"
        matches = regex.finditer(regex_str, in_str)
        res = []
        for m in matches:
            res.append(m.group(0))
        return res

class CommandInterpreter(Interpreter):
    def __init__(self):
        regex_str = "[a-zA-Z]*(\s)*\{[^\\\\\{\}]*\}"
        super().__init__(regex_str)

if __name__ == "__main__":
    # regex_str = "(.)* \s*\({1}([a-zA-Z](\s*,\s*)*)+(\){1})\s*={1})\s*(\((([^=\(\)]*)|(?6))*\))"
    # print(regex_str[47])
    fi = FunctionInterpreter()
    checked_function = "f1(x,x) = ((x, ,,,,,x)"
    a = fi.match(checked_function)
    b = fi.partial_match_name(checked_function)
    c = fi.partial_match_variables(checked_function)
    d = fi.partial_match_function(checked_function)
    print(a)
    print(b)
    print(c)
    print(d)