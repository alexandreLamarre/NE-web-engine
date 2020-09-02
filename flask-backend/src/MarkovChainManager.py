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
                    states.append(el.replace(":", ""))
                    if transition_row:
                        transitions.append(transition_row)
                        transition_row = []
                else:
                    el = el.replace(")", "")
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
            ## we can truncate down the number of transitions
            if len(transitions[i]) > len(states[i]):
                transitions[i] = transitions[i][:len(states[i])]
            elif len(transitions[i]) < len(states[i]):
                length_goal = len(states[i]) - len(transitions[i])
                while(length_goal != len(states[i])):
                    transitions[i].append(0)
                    length_goal += 1
            transitions[i] = self.normalize(transitions[i])
            try:
                c = Chain(states[i], transitions[i])
                chain_list.append(c)
            except:
                ## Should only get executed if something goes horribly wrong
                self.Error_stack.push_error("Number of states and transitions did not match in {}: {} vs {}".format((states[i], transitions[i]),len(states[i]), len(transitions[i])))
        return chain_list

    def normalize(self, transitions):
        """
        int[] [] -> int[] []
        Normalizes all the nested lists of transitions probabilities"""
        new_transitions = []
        for t in transitions:
            new_transition_row = []
            normalizing_constant = sum(t)
            for i in range(len(t)):
                new_transition_row.append(t[i]/normalizing_constant)
            new_transitions.append(new_transition_row)
        return new_transitions

    def get_interpreted(self):
        """
        Displays the markov chain in a matrix style
        """
        # output_strings = []
        # for mc in self.chain_list:
        #     max_str_len_column = []
        #     s = mc.get_states()
        #     t = mc.get_transitions()
        #
        #     for i in range(len(s)):
        #         max_len = 0
        #         for tr in t:
        #             max_len= max(len(str(tr[i])), max_len)
        #         max_str_len_column.append(max_len)
        #     max_len_state = 0
        #     for st in s:
        #         max_len_state = max(len(st), max_len_state)
        #     first_row = "" + " "*max_len_state
        #
        #     for i in range(len(s)):
        #         padding = max_str_len_column[i] - len(s[i])
        #         first_row += " "*(padding//2) + s[i] + " "*(padding//2)
        #     print(max_len_state)
        #     print(max_str_len_column)
        #     print(first_row)







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
    M = MarkovChainManager("(a: 0.1 0.4 0.5 b: 0.2 0.4 0.4 c: 0.2 0.2 0.2)")
    print("state_list test")
    print(M.state_list)
    print("transition list test")
    print(M.transitions_list)
    print("chain list test")
    print(M.chain_list)
    print("normalize test")
    print(M.normalize([[1.5, 1.4, 1.3]]))
    print("\n")

    M = MarkovChainManager("(one: 1 1 1 1 1 two: 1 1 1 1 1 three 1 1 1 1 1 four 1 1 1 1 1 five 1 1 1 1 1) (a: 1 1 1 b: 1 2 3 c: 1 2 3)")
    M.get_interpreted()
    print(M.chain_list)
    end_time = os.times()[0]
    print("{} seconds".format(end_time- start_time))