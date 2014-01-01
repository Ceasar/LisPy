"""
Tool for evaluating an abstract syntax tree.

The synthesis part constructs the desired target program from the intermediate
representation and the information in the symbol table.
"""

# TODO: If we are super lazy about evaluation and stored function needs to be
# called with what arguments, we can figure out what to memoize

"""
Evaluate a program.

>>> evaluate(1)
1
>>> evaluate(['define 'x', 1])
>>> evaluate(['do', ['define 'x', 1], 'x'])
1
>>> evaluate(['if', ['==', 0, 0], 1, 2])
1
>>> evaluate(['if', ['==', 0, 1], 1, 2])
2
"""




class Environment(dict):
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, name):
        if name in self:
            return self
        else:
            if self.outer:
                return self.outer.find(name)
            else:
                raise NameError("name '%s' is not defined" % name)
