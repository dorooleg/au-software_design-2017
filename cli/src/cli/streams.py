
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
