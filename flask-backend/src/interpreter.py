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

    def get_interpreted(self):
        pass

    def get_uninterpreted(self):
        pass

class FunctionInterpreter(Interpreter):
    def __init__(self):
        super().__init__("(([a-zA-Z]|[0-9])+\s*\({1}([a-zA-Z](\s*,\s*)*)+(\){1})\s*={1})\s*(\((([^=\(\)]*)|(?6))*\))")

class CommandInterpreter(Interpreter):
    def __init__(self):
        super().__init__("[a-zA-Z]*\{[^\\\\\{\}]*\}")

