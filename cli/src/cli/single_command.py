"""Concrete SingleCommand's and their Factory.

Since there can be many SingleCommand's (cat,
echo, wc, ..., you name it), it is convenient
to have them in a separate module.

There is a Factory class that "knows"
how to choose an appropriate Command
given it's string representation.
"""
import logging
import os.path
import os
import subprocess

from cli.commands import SingleCommand
from cli.exceptions import ExitException


class CommandExternal(SingleCommand):
    """An external command (not described in shell).

    Command args:
        0 -- a command's name. This name is searched
            via joining the current working directory
            with the command name (i.e. it must be somewhere
            in the current directory).
        1..n -- command's arguments. There can be any arguments
            depending on a command.
    """

    COMMAND_FAILED = 1

    def run(self, input_stream, env):
        pass


class SingleCommandFactory:
    """A class that is repsonsible for building Single Commands.

    This class knows which commands exist in shell.
    """

    registered_commands = dict()

    @staticmethod
    def build_command(cmd_name_and_args_lexem_lst):
        """Build a single command out of list of lexems representing it's arguments.

        Args:
            cmd_name_and_args_lexem_lst (list[:class:`lexer.Lexem`]): a list
                of lexems. The first one must be STRING that represents a command
                name. The rest are STRING or QUOTED_STRING 's.

        All string representations of lexems are passed to a corresponding
        SingleCommand descendant.
        """
        cmd_name = cmd_name_and_args_lexem_lst[0]
        cls = SingleCommandFactory._get_command_class_by_name(cmd_name.get_value())
        string_repr_of_all_args = [x.get_value() for x in cmd_name_and_args_lexem_lst]

        return cls(string_repr_of_all_args)


    @staticmethod
    def _get_command_class_by_name(cmd_name):
        cmd_cls = SingleCommandFactory.registered_commands.get(cmd_name, CommandExternal)
        logging.debug('SingleCommandFactory:\
                Class {} is responsible for invoking command {}'.format(
                    cmd_cls, cmd_name))
        return cmd_cls


def _register_single_command(command_name):
    """Every shell command with a name (e.g. `cat`) must be registered using this decorator.
    """

    def class_decorator(cls):
        SingleCommandFactory.registered_commands[command_name] = cls
        return cls

    return class_decorator


@_register_single_command('echo')
class CommandEcho(SingleCommand):
    """`echo` command: prints it's arguments.

    Command args:
        0 -- `echo`
        1..n -- strings. Those strings are written to the output, space-separated.

    """
 
    def run(self, input_stream, env):
        pass


@_register_single_command('wc')
class CommandWc(SingleCommand):
    """`wc` command: count the number of words, characters and lines.

    Command args:
        0 -- `wc`

        1 (optional) -- a filename. If provided, then `wc` will
            count the number of characters in this file. Otherwise,
            it will take it's input.
            Can be relative or absolute.

    Returns `FILE_NOT_FOUND` exit code if file was provided,
    but was not found.
    """

    FILE_NOT_FOUND = 1
 
    def run(self, input_stream, env):
        pass


@_register_single_command('cat')
class CommandCat(SingleCommand):
    """`cat` command: print it's input or file contents.

    Command args:
        0 -- `cat`

        1 (optional) -- a filename. If provided, `cat` will
            output that file's contents. Otherwise,
            it will print it's input.
            Can be relative or absolute.

    Returns `FILE_NOT_FOUND` exit code if file was provided,
    but was not found.
    """

    FILE_NOT_FOUND = 1
 
    def run(self, input_stream, env):
        pass


@_register_single_command('pwd')
class CommandPwd(SingleCommand):
    """`pwd` command: print the current working directory.
    """
 
    def run(self, input_stream, env):
        pass


@_register_single_command('exit')
class CommandExit(SingleCommand):
    """`exit` command: exit shell.

    Performs exiting via throwing an exception,
    so all further commands are not run.
    """
 
    def run(self, input_stream, env):
        pass


@_register_single_command('cd')
class CommandCd(SingleCommand):
    """`cd` command: change directory.

    Command args:
        0 -- `cd`
        1 -- a new filepath. Can be relative or absolute.
    """
 
    def run(self, input_stream, env):
        pass
