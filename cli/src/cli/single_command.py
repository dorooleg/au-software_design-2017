"""Concrete SingleCommand's and their Factory.

Since there can be many SingleCommand's (cat,
echo, wc, ..., you name it), it is convenient
to have them in a separate module.

There is a Factory class that "knows"
how to choose an appropriate Command
given it's string representation.
"""
from cli.commands import SingleCommand

import logging


class CommandExternal(SingleCommand):

    def run(self, input_stream, env):
        pass


class SingleCommandFactory:

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

    def class_decorator(cls):
        SingleCommandFactory.registered_commands[command_name] = cls
        return cls

    return class_decorator


@_register_single_command('echo')
class CommandEcho(SingleCommand):
    
    def run(self, input_stream, env):
        pass


@_register_single_command('wc')
class CommandWc(SingleCommand):
    
    def run(self, input_stream, env):
        pass


@_register_single_command('cat')
class CommandCat(SingleCommand):
    
    def run(self, input_stream, env):
        pass


@_register_single_command('pwd')
class CommandPwd(SingleCommand):
    
    def run(self, input_stream, env):
        pass


@_register_single_command('exit')
class CommandExit(SingleCommand):
    
    def run(self, input_stream, env):
        pass


@_register_single_command('cd')
class CommandCd(SingleCommand):
    
    def run(self, input_stream, env):
        pass
