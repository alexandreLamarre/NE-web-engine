import numpy as np
import pandas as pd
import io
import base64
from random import seed
from random import random
import matplotlib.pyplot as plt

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
        self.matrix = self.process_transitions(transitions)
        markov_chain = list(zip(states, transitions))
        efficient_chain = {}
        for m in markov_chain:
            efficient_chain[m[0]] = m[1]
        self._transitions = efficient_chain

    def convert_plot_to_base64(self,figure):
        buf = io.BytesIO()

        figure.savefig(buf, format = "png")
        base64_string = base64.b64encode(buf.getvalue())
        return str(base64_string)[2:-1]

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

    def get_interpreted(self):
        output_str = "<br>"
        states = self.get_states()
        transitions = self.get_transitions()

        output_str += "Start state: " + states[0] + "<br>"
        for i in range(len(states)):
            for j in range(len(states)):
                output_str += "{} -> {} : {}  ".format(states[i], states[j], transitions[states[i]][j])
            output_str += "<br>"
        return output_str

    def process_transitions(self, transitions):
        return np.array(transitions)

    def approximate_distribution(self, num_orbits = 1000, orbit_length = 10000):
        hits_dict = {}
        states = self.get_states()
        ## initialize number of times we got resultant node
        for el in states:
            hits_dict[el] = 0

        for no in range(num_orbits):
            start_state = self._states[0]
            next_state = self.step(start_state)
            for ol in range(orbit_length-1):
                next_state = self.step(next_state)

            hits_dict[next_state] += 1

        ##TODO iterate over dict
        output_str = ""
        for s in states:
            output_str += "{}: {} ".format(s, hits_dict[s]/num_orbits)
        return output_str

    def start_state_to_transition_matrix(self):
        matrix = [1.0]
        for i in range(len(self.get_states()) - 1):
            matrix.append(0.0)
        return matrix

    def stationary_distribution(self, num_exponentiations=50):
        #Prevent any kind of crazy matplotlib memory leaks (which seem to happen pretty frequently)
        plt.close("all")
        # Stochastic matrix P
        P = self.get_transition_matrix()
        s = self.start_state_to_transition_matrix()
        state = np.array([s])
        stateHist = state

        dfStateHist = pd.DataFrame(state)
        distribution_hist = [[0]*len(self.get_states())]

        for x in range(num_exponentiations):
            state = np.dot(state,P)
            stateHist = np.append(stateHist,state,axis = 0)

            # dfDistrHist.plot()
        dfDistrHist = pd.DataFrame(stateHist, columns=self.get_states())
        dfDistrHist.plot(alpha = 0.7)
        ax = plt.gca()
        ax.set_ylabel("Probability")
        plt.title("Stationary Distribution")
        # plt.show()
        ##Calculate the actual value of the stationary distribution
        distr_values = self.calculate_stationary_distribution(P)


        figure = plt.gcf()
        output_plot = self.convert_plot_to_base64(figure)
        plt.close("all")

        return output_plot, distr_values

    def calculate_stationary_distribution(self, matrix):
        """
        Solves the following for pi, where pi = startstate * stochastic_matrix^n as n-> infinity
        Using Rouche-Capelli equation solutions, after simplification
        """
        A = np.append(np.transpose(matrix) - np.identity(len(self.get_states())), [[1]*len(self.get_states())], axis = 0)
        b = []
        for i in range(len(self.get_states())):
            b.append(0)
        b.append(1)
        b = np.transpose(np.array(b))
        return np.linalg.solve(np.transpose(A).dot(A), np.transpose(A).dot(b))

    def simulation_history(self, num_simulations = 1000, rand_seed = None):
        ## Fix any potential memory leaks create by matplotlib (which is wayy more often than you would like)
        plt.close("all")

        P = self.get_transition_matrix()
        default = []
        for i in range(len(self.get_states())):
            temp_row = []
            for j in range(len(self.get_states())):
                temp_row.append(0)
            default.append(temp_row)

        stateChangeHist = np.array(default)
        state = np.array([self.start_state_to_transition_matrix()])
        currentState = 0
        stateHist = state
        dfStateHist = pd.DataFrame(state)
        distr_hist = [[0]*len(self.get_states())]

        if rand_seed:
            seed(rand_seed)

        def simulate_multinomial(vmultinomial):
            r=np.random.uniform(0.0, 1.0)
            CS= np.cumsum(vmultinomial)
            CS= np.insert(CS,0,0)
            m = (np.where(CS<r))[0]
            nextState = m[len(m)-1]
            return nextState

        for x in range(num_simulations):
            currentRow = np.ma.masked_values((P[currentState]), 0.0)
            nextState = simulate_multinomial(currentRow)

            stateChangeHist[currentState,nextState] += 1
            # construct array of 0's that don't point to the same place in memory
            temp_array = []
            for i in range(len(self.get_states())):
                temp_array.append(0)

            state =np.array([temp_array])
            state[0,nextState] = 1.0

            stateHist = np.append(stateHist, state, axis = 0)
            currentState=nextState

            totals = np.sum(stateHist, axis = 0)
            gt = np.sum(totals)
            distr = totals/gt
            distr = np.reshape(distr, (1,len(self.get_states())))
            distr_hist = np.append(distr_hist, distr, axis = 0)

        dfDistrHist = pd.DataFrame(distr_hist, columns = self.get_states())

        dfDistrHist.plot(title = "Simulation History")
        ax = plt.gca()
        ax.set_ylabel("Probability")
        plt.show()
        figure = plt.gcf()

        output_plot = self.convert_plot_to_base64(figure)
        return output_plot


    def distribution(self):
        pass

    def individual_state_properties(self):
        pass

    def is_regular(self):
        pass

    def get_transition_matrix(self):
        return self.matrix

    def __repr__(self):
        return str(self.get_transitions())
