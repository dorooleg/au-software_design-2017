from abc import ABCMeta, abstractmethod
import logging

"""Abstractions of commands and their results.

In principle, we have two types of commands:

    - a single command, like ``wc`` or ``cat``. It accepts
        input, returns something, etc. 
        This is represented by :class:`.SingleCommand`.

    - a combination of commands, like ``pwd | wc``. It consists
        of several commands that interact with each other
        by some rules. This is represented by :class:`.ChainCommand`.

Since each command has the same interface (i.e. it can run,
given input and environment), the above classes share a 
common base class, which represents an abstract command -
:class:`.RunnableCommand`.

This module also contains an abstraction of a command run
result.
"""


class RunnableCommandResult:
    """Represents result of invoking a :class:`.RunnableCommand`.

    It is more convenient to have a single class than a bunch
    of values (output, return code, etc.).
    """

    def __init__(self, output_stream, new_env, ret_code):
        """ Create CommandResult out of <output_stream, new_env, ret_code>.

        `output_stream` (:module:`streams.OutputStream`): an output stream
            of the program;
        `new_env` (:module:`environment.Environment`): a new environment
            in which shell should operate after executing the program.
            For example:
                ``x=1``
            should return a new environment with $x equal to `1`;
        `ret_code` (int): a return code.
        """
        self._output_stream = output_stream
        self._new_env = new_env
        self._ret_code = ret_code

    def get_return_code(self):
        """Getter for the return code.
        """
        return self._ret_code

    def get_output(self):
        """Read the command's output.

        Returns:
            str: a string representation of output.
        """
        return self._output_stream.get_output()

    def get_derived_input_stream(self):
        """Get an InputStream instance based on this program's OutputStream.
        """
        return self._output_stream.to_input_stream()

    def get_result_environment(self):
        """Getter for the new environment.
        """
        return self._new_env


class RunnableCommand(metaclass=ABCMeta):

    @abstractmethod
    def run(self, input_stream, env):
        return NotImplemented


class CommandChain(RunnableCommand):

    def __init__(self, cmd1, cmd2):
        self.cmd_left = cmd1
        self.cmd_right = cmd2


class ChainPipe(CommandChain):

    def run(self, input_stream, env):
        pass


class SingleCommand(RunnableCommand):

    def __init__(self, args_lst):
        self.args_lst = args_lst
