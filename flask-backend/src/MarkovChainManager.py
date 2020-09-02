from src.DataManager import DataManager
from src.interpreter import ChainInterpreter
class MarkovChainManager(ChainInterpreter, DataManager):
    def __init__(self):
        super().__init__()

    def get_interpreted(self):
        pass

    def get_errors(self):
        pass

    def get_uninterpreted(self, in_str):
        pass

    def process_uninterpreted(self, uninterpreted_string):
        pass

    def generate_reason_uninterpreted(self, unintepreted_string):
        pass