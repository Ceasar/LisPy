

class Context(dict):
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
