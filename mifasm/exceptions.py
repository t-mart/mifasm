class WidthError(ValueError):
    def __init__(self, i, width, *args, **kwargs):
        super(WidthError, self).__init__("%d cannot be represented in width %d" % (i, width), *args, **kwargs)
