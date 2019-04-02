Graph Theory project Regular expressions and Thompsons construction

Note: Typo in name will be corrected after project is marked.

To run project type python grapTheoryProject.py

Project has strings already defined and ready for testing.

Project is to implement Thompsons Construction to build non-deterministic finite automata from regular expressions.

Program can be broken down into 4 sections:

1. Implement shunting yard algorithm as a function to convert infix regular expressions to postfix notation.

Ex: (a.b)|(c*.d) - to - ab.c*d.|

2. Define classes to represent an NFA and a State

3. Implement Thompsons construction as compile function to build an NFA from a postfix string.

4. Implement Follow E's function to return the set of states that can be reached following an Empty string

5. Implement match function to match a string to an infix regular expression
