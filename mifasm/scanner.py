import re

COMMENT_DELIMETER = '#'

class Scanner(object):
    content_pattern = re.compile('\w')
    def __init__(self, input_f):
        self.input_f = input_f

    def readlines(self):
        for line in self.input_f.readlines():
            cleansed = Scanner.cleanse_line(line)
            if Scanner.line_has_content(cleansed):
                yield cleansed

    @staticmethod
    def cleanse_line(line):
        comment_index = line.find(COMMENT_DELIMETER)
        if comment_index >= 0:
            line = line[:comment_index]
        return line.strip()

    @staticmethod
    def line_has_content(line):
        return Scanner.content_pattern.search(line)

