# Arron Healy 
# shunting algorithm
# convert strings from infix to postfix
 
def shunt(infix):

    specials = {
        "*": 50,
        ".": 40,
        "|": 30
    }

    postfix = ""
    stack = ""

    for i in infix:
        if i == "(":
            stack += i
        elif i == ")":
            while stack[-1] != "(":
                postfix, stack = postfix + stack[-1], stack[:-1]
            stack = stack[:-1]
        elif i in specials:
            while stack and specials.get(i, 0) <= specials.get(stack[-1], 0):
                postfix, stack = postfix + stack[-1], stack[:-1]
            stack = stack + i
        else:
            postfix = postfix + i

    while stack:
        postfix, stack = postfix + stack[-1], stack[:-1]
    
    return postfix



print(shunt("(a.b)|(c*.d)"))

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
    stack = []

    for c in postfix:
        if c == '.':
            # pop 2 nfa's off the stack
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            # connect first nfa's accept state to the seconds initial
            nfa1.accept.edge1 = nfa2.initial
            # push nfa to stack
            stack.append(nfa(nfa1.initial, nfa2.accept))
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

print(compile("ab.cd.|"))