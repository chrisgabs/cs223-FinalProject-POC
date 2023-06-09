class TSAFM_Ordinances:
    """
    Implementation of a Non-Deterministic Transition-Assigned Finite State Machine (Mealy Automaton)

    where:
    Q - Set of states
    S - input alphabet
    R - output alphabet
    f - state transition function (Q x S -> Q)
    g - output function (Q x S -> R)
    qi - initial state
    """

    def __init__(self, Q, S, R, f, g, qi):
        self.Q = Q
        self.S = S
        self.R = R
        self.f = f
        self.g = g
        self.q0 = qi

    def run(self, input_str):
        """
        Processes an input string and returns the output generated by the FSM.

        Returns:
        - output: the output generated by the FSM for the input string
        """
        q = self.q0
        ordinance_codes = []
        candidate_string = ""
        for symbol_raw in input_str.split(" "):
            token = None
            symbol = symbol_raw.lower()

            if symbol in self.S:
                token = symbol
            elif len(symbol) > 1:
                if (symbol.isdigit() or symbol[:-1].isdigit()) and symbol[-2].isdigit():
                    token = "_%number%_"

            q_next = self.f.get((q, token), None)
            if q_next is None:
                q = "A"
                candidate_string = ""
                continue

            if q_next == "A":
                # Remove trailing comma or period in year if there is any
                if symbol[-1] == "," or symbol[-1] == ".":
                    symbol_raw = symbol_raw[:-1]
                candidate_string += symbol_raw + " "
                ordinance_codes.append(candidate_string.strip())
                candidate_string = ""
                q = q_next
                pass

            # If there is a new state, then append current word to 
            # candidate_string
            candidate_string += symbol_raw + " "
            q = q_next

        return ordinance_codes


# ordinances
fsm_ordinances = TSAFM_Ordinances(
    Q = {'A', 'B', 'C', 'D', 'E', 'F', 'G'},
    S = {'ordinance', 'no.', '_%number%_', 'series', 'of', ''},
    R = {True, False},
    f = {('A', 'ordinance'): 'B', ('B', 'no.'): 'C', ('C', '_%number%_'): 'D', ('D', 'series'): 'E', ('E', 'of'): 'G', ('G', '_%number%_'): 'A'},
    g = {('A', 'ordinance'): True, ('B', 'no.'): True, ('C', '_%number%_'): True, ('D', 'series'): True, ('E', 'of'): True, ('G', '_%number%_'): True}, 
    qi ='A')


# --------------------------------------------------------------------------------


# resolutions
fsm_resolutions = TSAFM_Ordinances(
    {'A', 'B', 'C', 'D', 'E', 'F', 'G'},
    {'resolution', 'no.', '_%number%_', 'series', 'of', ''},
    {True, False},
    {('A', 'resolution'): 'B', ('B', 'no.'): 'C', ('C', '_%number%_'): 'D', ('D', 'series'): 'E', ('E', 'of'): 'G', ('G', '_%number%_'): 'A'},
    {('A', 'resolution'): True, ('B', 'no.'): True, ('C', '_%number%_'): True, ('D', 'series'): True, ('E', 'of'): True, ('G', '_%number%_'): True},
    'A')


# --------------------------------------------------------------------------------

from unidecode import unidecode

class FSA_CandidateTitleToken:
    def __init__(self, Q, S, R, f, g, qi):
        self.Q = Q
        self.S = S
        self.R = R
        self.f = f
        self.g = g
        self.q0 = qi

    def run(self, input_str):
        q = self.q0
        out = 0
        for token in input_str:
            # standardize font style
            token = unidecode(token)
            # check if character is lower alphabet
            if ord(token) > 96 and ord(token) < 123:
                token = "lower"
            # check if character is upper alphabet
            elif ord(token) > 64 and ord(token) < 91:
                token = "upper"
            # check if character is numerical
            elif ord(token) > 47 and ord(token) < 58:
                token = "numnerical"
            # else, character is special character
            else:
                token = "special"
            q_next = self.f.get((q, token), None)
            out = self.g.get((q, token), None)
            q = q_next
            if out == False:
                return False
        return True
    

# Define the parameters for the TSAFM
Q = {'A', 'B', 'C'}
S = {"lower", "upper", "numerical", "special"}
R = {True, False}
f = {('A', 'lower'): 'A', ('A', 'upper'): 'B', ('A', 'numerical'): 'B', ('A', 'special'): 'C', 
     ('B', 'upper'): 'B', ('B', 'numerical'): 'B', ('B', 'special'): 'B', ('B', 'lower'): 'A', 
     ('C', 'lower'): 'A', ('C', 'upper'): 'B', ('C', 'numerical'): 'B', ('C', 'special'): 'C'}
g = {('A', 'lower'): False, ('A', 'upper'): True, ('A', 'numerical'): True, ('A', 'special'): False, 
     ('B', 'upper'): True, ('B', 'numerical'): True, ('B', 'special'): True, ('B', 'lower'): False, 
     ('C', 'lower'): False, ('C', 'upper'): True, ('C', 'numerical'): True, ('C', 'special'): False}
qi = 'A'

# Create an instance of the TSAFM
fsm_candidates = FSA_CandidateTitleToken(Q, S, R, f, g, qi)


# --------------------------------------------------------------------------------

class FSA_Title:
    def __init__(self, Q, S, R, f, g, qi):
        self.Q = Q
        self.S = S
        self.R = R
        self.f = f
        self.g = g
        self.q0 = qi

    def run(self, input_str, fsa_validator):
        q = self.q0
        candidate_words = ""
        for token in input_str.split(" "):
            is_candidate = "valid" if fsa_validator.run(token) else "invalid"
            if is_candidate == "invalid":
                break
            q_next = self.f.get((q, is_candidate), None)
            out = self.g.get((q, is_candidate), None)
            if out == "0":
                candidate_words = ""
            elif out == "1":
                candidate_words += token + " "
            else:
                return candidate_words.strip()
            q = q_next
        return candidate_words.strip()
    

# Define the parameters for the TSAFM
Q = {'A', 'B', 'C', 'D'}
S = {'valid', 'invalid'}
R = {'0', '1', '2'}
f = {('A', 'valid'): 'B', ('A', 'invalid'): 'A', 
     ('B', 'valid'): 'C', ('B', 'invalid'): 'A',
     ('C', 'valid'): 'C', ('C', 'invalid'): 'D',
     ('D', 'valid'): 'A', ('D', 'invalid'): 'A',}
g = {('A', 'valid'): '1', ('A', 'invalid'): '0', 
     ('B', 'valid'): '1', ('B', 'invalid'): '0',
     ('C', 'valid'): '1', ('C', 'invalid'): '2',
     ('D', 'valid'): '0', ('D', 'invalid'): '0',}
qi = 'A'

# Create an instance of the TSAFM
fsm_title = FSA_Title(Q, S, R, f, g, qi)

# --------------------------------------------------------------------------------

class FSA_Date1:
    def __init__(self, Q, S, R, f, g, qi):
        self.Q = Q
        self.S = S
        self.R = R
        self.f = f
        self.g = g
        self.q0 = qi

    def run(self, input_str):
        q = self.q0
        accepted_words = []
        candidate_words = ""
        for token in input_str.split(" "):
            symbol = unidecode(token).lower().strip()
            stimulus = "INVALID"
            # check if symbol is month
            if symbol in ["january", "february", "march", "april", 
                          "may", "june", "july", "august", 
                          "september", "october", "november", "december"]:
                stimulus = "MONTH"

            # check if symbol is candidate year
            elif len(symbol) == 4 or len(symbol) == 5:
                if (symbol.isdigit() or symbol[:-1].isdigit()):
                    stimulus = "YEAR"

            # Check if symbol is valid number candidate
            elif len(symbol) > 1:
                if symbol[:-1].isdigit() and symbol[-1] == ",":
                    stimulus = "DAY"


            q_next = self.f.get((q, stimulus), "A")
            out = self.g.get((q, stimulus), "0")

            if out == "0":
                candidate_words = ""
            elif out == "1":
                candidate_words += token + " "
            # if accepting state
            if q_next == "D":
                accepted_words.append(candidate_words.strip())
            q = q_next
        
        return accepted_words
    
# Create an instance of the TSAFM
fsm_dates1 = FSA_Date1(
    Q = {'A', 'B', 'C', 'D'}, 
    S = {'MONTH', 'DAY', 'YEAR', "INVALID"}, 
    R = {'0', '1', '2'}, 
    f = {('A', 'MONTH'): 'B', ('B', 'DAY'): 'C', ('C', 'YEAR'): 'D'}, 
    g = {('A', 'MONTH'): '1', ('B', 'DAY'): '1', ('C', 'YEAR'): '1', 
         ('D', 'MONTH'): '2', ('D', 'DAY'): '2', ('D', 'YEAR'): '2', ('D', 'INVALID'): '2'}, 
    qi= 'A')

# --------------------------------------------------------------------------------

class FSA_Date2:
    def __init__(self, Q, S, R, f, g, qi):
        self.Q = Q
        self.S = S
        self.R = R
        self.f = f
        self.g = g
        self.q0 = qi

    def run(self, input_str):
        q = self.q0
        out = False
        tokens = unidecode(input_str).split("/")

        if len(tokens) != 3:
            return out
        for i,token in enumerate(tokens):
            symbol = None

            # if to be check is either day or month
            if i != 2:
                # if the token is a digit, check validity
                if token.isdigit():
                    if int(token) > 0 and int(token) < 32:
                        symbol = "DD"
                    if int(token) > 0 and int(token) < 13:
                        symbol = "MM"
                    if int(token) < 0 or int(token) > 99 or token[0] == "0":
                        symbol = "INVALID"
                else:
                    symbol = "INVALID"
            # if to be checked is year
            else:
                # if token's last element is a digit
                if token[-1].isdigit():
                    if len(token) == 2:
                        symbol = "YY"
                # if token's last element is not a digit
                else:
                    # check if characters preceding it is a digit
                    if token[:-1].isdigit():
                        if len(token[:-1]) == 2:
                            symbol = "YY"
                        else:
                            symbol ="INVALID"
                    else:
                        symbol = "INVALID"

            q_next = self.f.get((q, symbol), "A")
            out = self.g.get((q, symbol), False)
            
            q = q_next
        return out
    
fsm_dates2 = FSA_Date2(
    Q = {'A', 'B', 'C', 'D'}, 
    S = {'MM', 'DD', 'YY', "INVALID"}, 
    R = {False, True}, 
    f = {('A', 'MM'): 'B', ('B', 'DD'): 'C', ('C', 'YY'): 'D',
         ('A', 'DD'): 'A', ('C', 'MM'): 'D', ('C', 'DD'): 'D', 
         ('B', 'MM'): 'C'}, 
    g = {('C', 'YY'): True, ('C', 'MM'): True, ('C', 'DD'): True },
    qi = 'A')

# --------------------------------------------------------------------------------

class TSM_Proclamations:
    """
    Implementation of a Non-Deterministic Transition-Assigned Finite State Machine (Mealy Automaton)

    where:
    Q - Set of states
    S - input alphabet
    R - output alphabet
    f - state transition function (Q x S -> Q)
    g - output function (Q x S -> R)
    qi - initial state
    """

    def __init__(self, Q, S, R, f, g, qi):
        self.Q = Q
        self.S = S
        self.R = R
        self.f = f
        self.g = g
        self.q0 = qi

    def run(self, input_str):
        """
        Processes an input string and returns the output generated by the FSM.

        Returns:
        - output: the output generated by the FSM for the input string
        """
        q = self.q0
        proclamation_codes = []
        candidate_string = ""
        for symbol_raw in input_str.split(" "):
            token = None
            symbol = unidecode(symbol_raw).lower()

            # Check if symbol is reserved word
            if symbol in self.S:
                token = symbol
            # Check if symbol is valid number candidate
            elif len(symbol) > 1:
                # Checks if the symbol is a number, while taking into consideration a 
                # possible trailing comma or period in the string
                if (symbol.isdigit() or symbol[:-1].isdigit()) and symbol[-2].isdigit():
                    token = "_%number%_"
                    if symbol[-1].isdigit():
                        if len(symbol) == 4 and int(symbol) > 999 and int(symbol) < 3000:
                            token = "_%year%_"
                    else:
                        if len(symbol) == 5 and int(symbol[:-1]) > 999 and int(symbol[:-1]) < 3000:
                            token = "_%year%_"
            # If there is no next state given a current state and input,
            # Then go back to state A and reset candidate_string
            q_next = self.f.get((q, token), None)
            if q_next is None:
                q = "A"
                candidate_string = ""
                continue
            
            # if len(candidate_string) != 0:
            #     print(symbol_raw, q, token)
            # If the next state is A, this means that the candidate string 
            # is now a complete and valid ordinance code.
            # Append candidate_string to the list of ordinance codes taken
            # from given input.
            # Reset candidate string to empty string
            if q_next == "A":
                # Remove trailing comma or period in year if there is any
                if symbol[-1] == "," or symbol[-1] == ".":
                    symbol_raw = symbol_raw[:-1]
                candidate_string += symbol_raw + " "
                proclamation_codes.append(candidate_string.strip())
                candidate_string = ""
                q = q_next
                pass

            # If there is a new state, then append current word to 
            # candidate_string
            candidate_string += symbol_raw + " "
            q = q_next

        return proclamation_codes
    
fsm_proclamations = TSM_Proclamations(
    Q = {'A', 'B', 'C', 'D', 'E', 'F'}, 
    S = {'proclamation', 'no.', '_%number%_', 's.', '_%year%_'}, 
    R = {False, True}, 
    f = {('A', 'proclamation'): 'B', ('B', 'no.'): 'C', ('C', '_%number%_'): 'D', ('C', '_%year%_'): 'D', ('D', 's.'): 'E', ('E', '_%year%_'): 'A'},
    g = {('A', 'proclamation'): True, ('B', 'no.'): True, ('C', '_%number%_'): True, ('D', 's.'): True, ('E', '_%year%_'): True},
    qi = 'A')