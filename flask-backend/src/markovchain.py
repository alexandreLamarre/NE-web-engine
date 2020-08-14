import numpy as np
""" Implementation of a Markov chain using states (which can be numbers, strings or
    even functions)"""


class Chain:
    """Object representing a stochastic markov chain"""
    def __init__(self, states, transitions):
        """ Initialize a markov chain with a list of states and list of list of
        transitions"""

        assert(len(states) == len(transitions)), \
            "number of states and transitions do not match"

        self._states = states
        markov_chain = list(zip(states, transitions))
        efficient_chain = {}
        for m in markov_chain:
            efficient_chain[m[0]] = m[1]
        self._transitions = efficient_chain

    def get_states(self):
        """ Getter function for the states of a markov chain"""
        return self._states

    def get_transitions(self):
        """ Setter function for the (states,transitions) pairs
        of the markov chain"""
        return self._transitions

    def pick_random(self, next_states):
        """ Given a list of transition functions (probabilities)
        choose a random next_state and return its index"""
        random_num = np.random.rand()
        previous = 0

        for i in range(len(next_states)):
            if random_num <= previous + next_states[i]:
                return i
            previous += next_states[i]

        # Error case
        return None

    def step(self, start_state):
        """ Computes one step along the markov chain"""
        dist = self._transitions[start_state]
        index = self.pick_random(dist)

        return self._states[index]

    def n_orbit(self, start_state, n=10):
        """ Returns a numpy array of a list of states"""
        res = [start_state]
        next_state = self.step(start_state)

        for i in range(n):
            res.append(next_state)
            next_state = self.step(next_state)

        return np.array(res)

    def __repr__(self):
        return str(self.get_transitions())
