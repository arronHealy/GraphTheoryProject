# Arron Healy 
# 3rd year Software
# Graph Theory Project
# Thompsons Construction


# shunting yard algorithm
# convert regular expressions from infix to postfix
 
def shunt(infix):

    """Shunting yard algorithm for converting regular expressions from infix to postfix"""

    # special characters and their precedence
    specials = {
        "*": 50,
        ".": 40,
        "|": 30
    }

    # return postfix string
    postfix = ""
    # operator stack
    stack = ""

    # loop for each character in input string
    for i in infix:
        # if open bracket push to stack
        if i == "(":
            stack += i
        # if closing bracket, pop from stack, push to output until opening bracket
        elif i == ")":
            while stack[-1] != "(":
                postfix, stack = postfix + stack[-1], stack[:-1]
            stack = stack[:-1]
        # if theres an operator, push to stack after popping lower or equal precedence operators from top of stack output
        elif i in specials:
            while stack and specials.get(i, 0) <= specials.get(stack[-1], 0):
                postfix, stack = postfix + stack[-1], stack[:-1]
            stack = stack + i
        # regular characters are pushed immediately to the output
        else:
            postfix = postfix + i

    # pop all remaining operator characters from stack
    while stack:
        postfix, stack = postfix + stack[-1], stack[:-1]
    
    return postfix



#print(shunt("(a.b)|(c*.d)"))

# Thompsons construction
# build nfa's from postfix regular expressions

# construction to determine whether state should be accepted

# represents a state with 2 arrows, labelled by label.
# use None for a label representing 'e' empty string arrows
class state:
    label = None
    edge1 = None
    edge2 = None

# nfa represented ny its initial & accept state
class nfa:
    initial = None
    accept = None

    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept


def compile(postfix):

    """Compiles a postfix regular expression into a NFA"""

    stack = []

    for c in postfix:
        # dot operator concatenates 2 nfa's together
        if c == '.':
            # pop 2 nfa's off the stack
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            # connect first nfa's accept state to the seconds initial
            nfa1.accept.edge1 = nfa2.initial
            # push nfa to stack
            stack.append(nfa(nfa1.initial, nfa2.accept))

        # OR operator allows for alternation between nfa's
        elif c == '|':
            # pop 2 nfa's off the stack
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            
            # create a new initial state, connect it to initial states of the 2 nfa's popped from stack
            initial = state()
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial

            # create a new accept state, connecting the accept states of the 2 nfa's popped from the stack, to the new state. 
            accept = state()
            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept
            # push new nfa to the stack
            stack.append(nfa(initial, accept))

        # check for zero or more if * character encountered
        elif c == '*':
            # pop a single nfa off the stack
            nfa1 = stack.pop()
            
            # create new initial and accept state
            initial = state()
            accept = state()

            # join the new initial state to nfa1's initial state and the new accept state
            initial.edge1 = nfa1.initial
            initial.edge2 = accept

            # join the old accept state to the new accept state and nfa1's initial state
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept

            # push new nfa to stack
            stack.append(nfa(initial, accept))

        # check for one or more characters if + operator encountered
        elif c == "+":
            # pop a single nfa off the stack
            nfa1 = stack.pop()

            # create new initial and accept state
            initial = state()
            accept = state()

            # point new initial state edge1 to popped initial state 
            initial.edge1 = nfa1.initial

            # point popped accept states edge1 back to popped initial state
            nfa1.accept.edge1 = nfa1.initial

            # point popped nfa's accept state to new accept state
            nfa1.accept.edge2 = accept

            # push new nfa to stack
            stack.append(nfa(initial, accept))

        # check for zero or one character if ? encountered in expression
        elif c == "?":
            # pop a single nfa from the stack
            nfa1 = stack.pop()

            # create new initial and accept state
            initial = state()
            accept = state()

            # point new initial state edge1 to popped nfa's initial state 
            initial.edge1 = nfa1.initial

            # point new initial states edge2 to new accept state
            initial.edge2 = accept

            # point popped nfa's accept state edge1 to new accept state 
            nfa1.accept.edge1 = accept

            # push new nfa to stack
            stack.append(nfa(initial, accept))

        # create new nfa for literal characters
        else:
            # create new initial and accept state
            accept = state()
            initial = state()
            # join initial to accept state using an arrow labeled c 
            initial.label = c
            initial.edge1 = accept
            # push new nfa to stack
            stack.append(nfa(initial, accept))
        
    return stack.pop()

#print(compile("ab.cd.|"))

def followes(state):
    """Return the set of states that can be reached from the state following e arrows"""

    # create a new set, with state as its only member
    states = set()
    states.add(state)

    # check if state has arrows labelled e from it
    if state.label is None:
        # check if edge1 is a state
        # if theres an edge1, follow it
        if state.edge1 is not None:
            states |= followes(state.edge1)
        
        #if theres an edge2, follow it
        if state.edge2 is not None:
            states |= followes(state.edge2)

    # return set of states
    return states


def match(infix, string):

    """Matches string to infix regular expression"""

    # shunt and compile the regular expression
    postfix = shunt(infix)
    nfa = compile(postfix)

    # the current set of states and next set of states
    currentSet = set()
    nextSet = set()

    # add initial state to the current set of states
    currentSet |= followes(nfa.initial)

    # loop through each character in string
    for s in string:
        # loop through the current set of states
        for c in currentSet:
            # check if that state is labelled s.
            if c.label == s:
                # add the edge1 state to the next set
              nextSet |= followes(c.edge1)
        # set current to next, and clear out next
        currentSet = nextSet
        nextSet = set()

    # check if the accept state is in the set of current states
    return (nfa.accept in currentSet)


infixes = ['a.b.c*', 'a.b.c+', 'a.(b|d).c*', '(a.(b|d))', 'a.(b.b)*.c', 'a.b.c?']
strings = ['', 'abbc', 'abcc', 'abad', 'abbbc', 'ab', 'abc']


for i in infixes:
    for s in strings:
        print(match(i, s), i, s)