class MifasmError(Exception):
    pass


class AssemblySourceError(MifasmError):
    def __init__(self, line=-1, fpath='foo'):
        self.line = line
        self.fpath = fpath

        super(AssemblySourceError, self).__init__()

    def __str__(self):
        return "error with assembly source"

    @property
    def locator_prefix(self):
        return "%s L%d: " % (self.fpath, self.line)


class WidthError(AssemblySourceError, ValueError):
    def __init__(self, i, type, width, *args, **kwargs):
        self.i = i
        self.type = type
        self.width = width
        super(WidthError, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.locator_prefix + \
                "%d (%s) cannot be represented in %d bits" \
                % (self.i, self.type, self.width)


class BadValueError(AssemblySourceError, ValueError):
    def __init__(self, v, *args, **kwargs):
        self.v = v
        super(BadValueError, self).__init__(*args, **kwargs)

    def __str__(self):
        return "'%s' isn't a valid value" % (self.v)


class BadAddressRadixError(MifasmError):
    pass
