from src.DataManager import DataManager
from src.interpreter import ChainInterpreter
from src.markovchain import Chain
from src.Error_Stack import ErrorStack
import os

class MarkovChainManager(ChainInterpreter, DataManager):
    def __init__(self, input_string):
        super().__init__()
        self.Error_stack = ErrorStack()
        self.original_input = input_string
        self.interpreted = self.match(input_string)
        self.state_list, self.transitions_list = self.process_chain(self.interpreted)
        self.chain_list = self.create_chains(self.state_list, self.transitions_list)
        self.uninterpreted = self.process_uninterpreted(self.original_input)

    def process_chain(self, regex_string):
        """
        Takes the string matched by the regex in this objects interpreter super class
        and splits into [states],[transitions] to later instantiate Markov Chains
        """
        total_states = []
        total_transitions = []

        for r in regex_string:
            split_chain = r.split()
            states = []
            transitions = []
            transition_row = []
            for el in split_chain:
                if ":" in el:
                    el = el.replace(":", "")
                    el = el.replace("(", "")
                    el = el.replace(")", "")
                    el = el.strip()
                    if el:
                        states.append(el)
                    if transition_row:
                        transitions.append(transition_row)
                        transition_row = []
                else:
                    el = el.replace(")", "")
                    el = el.strip()
                    if el:
                        transition_row.append(float(el))
            if transition_row:
                transitions.append(transition_row)
            total_states.append(states)
            total_transitions.append(transitions)

        return total_states, total_transitions

    def create_chains(self, states, transitions):
        """
        Instantiates Markov chains using the processed array strings from process_chain
        """
        chain_list = []
        for i in range(min(len(states), len(transitions))):
            ## truncate/expand transition lists to the number of states
            len_difference = len(transitions[i]) - len(states[i])
            if len_difference>0:
                transitions[i] = transitions[i][:len(states[i])]
                self.Error_stack.push_errors("Too many transitions sets were specified for the set of states, \
                                                truncating last {} transition".format(len_difference))
            elif len_difference < 0:
                length_goal = len(states[i]) - len(transitions[i])
                self.Error_stack.push_error("Not enough transition sets were specified for the set of states, \
                                                        adding empty {} transition sets".format(len_difference))
                while(length_goal != len(states[i])):
                    transitions[i].append([])
                    length_goal += 1
            ## truncate/expand transitions [i][j] to match states[i] length
            for j in range(len(transitions[i])):
                len_difference = len(transitions[i][j]) - len(states[i])
                if len_difference>0:
                    self.Error_stack.push_error("Too many transitions specified for state '{}', truncating last \
                                                                {} transitions".format(states[i][j], len_difference))
                    transitions[i][j] = transitions[i][j][:len(states[i])]
                elif len_difference<0:
                    self.Error_stack.push_error("Not enough transitions specified for state '{}', padding with \
                                                                    {} zero transitions".format(states[i][j],len_difference))
                    length_goal = len(states[i]) - len(transitions[i][j])
                    while(length_goal != len(states[i])):
                        transitions[i][j].append(0)
                        length_goal += 1
            transitions[i] = self.normalize(transitions[i], i)
            try:
                c = Chain(states[i], transitions[i])
                chain_list.append(c)
            except:
                ## Should only get executed if something goes horribly wrong
                pass
        return chain_list

    def normalize(self, transitions, chain_number):
        """
        int[] [] -> int[] []
        Normalizes all the nested lists of transitions probabilities"""
        new_transitions = []
        for t in transitions:
            new_transition_row = []
            ##Todo make all entries in t positive
            pos_entries_t = [abs(e) for e in t]
            normalizing_constant = sum(pos_entries_t)
            if normalizing_constant == 0:
                self.Error_stack.push_error("State '{}' does not transition to anything, breaking the markov chain".format(self.state_list[chain_number][transitions.index(t)]))
            else:
                for i in range(len(t)):
                    new_transition_row.append(t[i]/normalizing_constant)
                new_transitions.append(new_transition_row)
        return new_transitions

    def get_interpreted(self):
        """
        (None) -> String
        Displays the markov chain in a matrix style

        """
        output_str = ""
        for m in self.chain_list:
            output_str += m.get_interpreted() +"\n"

        return output_str if output_str else "None"

    def get_uninterpreted(self):
        output_str = ""
        uninterpreted = self.uninterpreted
        return output_str

    def get_errors(self):
        output_str = self.Error_stack.get_errors() + "  "

        ## TODO check markov chains in chain list for errors

        return output_str


    def process_uninterpreted(self, uninterpreted_string):
        res = uninterpreted_string
        for i_text in self.interpreted:
            start_index = res.find(i_text)
            end_index = len(i_text)
            res = res[:start_index]+ " "+ res[end_index:]
        return res

    def generate_reason_uninterpreted(self, unintepreted_string):
        pass

if __name__ == "__main__":
    start_time = os.times()[0]
    M = MarkovChainManager("(a: 1 1 2 b: 1 1 1 c: 2 2 2 2 2 2 2)")
    for c in M.chain_list:
        c.stationary_distribution(20)
    end_time = os.times()[0]
    print("{} seconds".format(end_time - start_time))
    # print(M.get_interpreted())
    # print(M.get_interpreted())
    # print(M.get_errors())
    # for c in M.chain_list:
    #     res = c.approximate_distribution()
    #     print(res)
    # end_time = os.times()[0]
    #
    # print("{} seconds".format(end_time-start_time))
    # M = MarkovChainManager("(a: 0) (a: 0 0 1 b: 1 1 1 c: 2 2 2 2 2 2 2 )")

    # print("state_list test")
    # print(M.state_list)
    # print("transition list test")
    # print(M.transitions_list)
    # print("chain list test")
    # print(M.chain_list)
    # print("normalize test")
    # print(M.normalize([[1.5, 1.4, 1.3]]))
    # print("\n")
    # print(M.get_interpreted())
    #
    # M = MarkovChainManager("(one: 1 1 1 1 1 two: 1 1 1 1 1 three 1 1 1 1 1 four 1 1 1 1 1 five 1 1 1 1 1) (a: 1 1 1 b: 1 2 3 c: 1 2 3)")
    # M.get_interpreted()
    # print(M.chain_list)
    # # end_time = os.times()[0]
    # print("{} seconds".format(end_time- start_time))