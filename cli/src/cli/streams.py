"""Abstractions of command input and output.

Every command accepts some input and results
in some output. This module contains abstractions
on this ideas.
"""


class InputStream:

    def get_input(self):
        pass

    @staticmethod
    def get_empty_inputstream():
        pass


class OutputStream:

    def write(self, string):
        pass

    def write_line(self, string):
        self.write(string)
        self.write('\n')

    def to_input_stream(self):
        pass

    def read_output(self):
        pass
