
class ShellException(Exception):
    pass


class ParseException(ShellException):
    pass


class LexException(ShellException):
    pass


class ExitException(ShellException):
    pass
