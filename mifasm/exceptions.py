class AssemblySourceError(Exception):
    def __init__(self, line=0, fp='foo', *args, **kwargs):
        self.line = line
        self.fp = fp
        self.msg = "error with assembly source"

        super(AssemblySourceError, self).__init__(*args, **kwargs)

    def __str__(self):
        return "%s L%d: %s" % (self.fp, self.line, self.msg)

class WidthError(AssemblySourceError, ValueError):
    def __init__(self, i, type, width, *args, **kwargs):
        self.msg = "%d (%s) cannot be represented in %d bits" % (i, type, width),
        super(WidthError, self).__init__(*args, **kwargs)

class BadValueError(AssemblySourceError, ValueError):
    def __init__(self, v, *args, **kwargs):
        self.msg = "'%s' isn't a valid value" % (v)
        super(BadValueError, self).__init__(*args, **kwargs)

