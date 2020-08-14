import numpy as np
from src.markovchain import Chain


class IFS:
    """ Object representing a set of Iterated functions used to generate fractals """
    def __init__(self, funcs, transitions, start_func):
        """ Initialize an IFS from a list of python functions and a list of transitions"""
        assert(len(funcs) == len(transitions)), "number of functions and transitions are mismatched funcs: {}, tr: {}".format(len(funcs), len(transitions))
        self.funcs = funcs
        # Create a markov chain from these Iterated functions used to generate fractals
        self.chain = Chain(funcs, transitions)

        self.start = start_func

    def apply(self, point, funcs):
        for f in funcs:
            point = f(point)

        return point

    def render(self, N, start, num_appl):
        array = []
        for i in range(N):
            for j in range(N):
                funcs = self.chain.n_orbit(start, num_appl)
                sample_point = self.apply(np.array([i/N, j/N]), funcs)
                array.append(sample_point)
        return array

    def get_funcs(self):
        return self.funcs

    def get_chain(self):
        return self.chain

    def get_start_state(self):
        return self.start

    def __repr__(self):
        return self.chain
