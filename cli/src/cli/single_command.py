from commands import RunnableCommand


class SingleCommand(RunnableCommand):

    def __init__(self, args_lst):
        self.args_lst = args_lst


class CommandExternal(SingleCommand):
    pass


class SingleCommandFactory:
    registered_commands = dict()

    @staticmethod
    def get_command_class_by_name(cmd_name):
        cmd_cls = registered_commands.get(cmd_name, CommandExternal)
        logging.debug('Class {} is responsible for invoking command {}'.format(
            cmd_cls, cmd_name))
        return cmd_cls


def _register_single_command(command_name):

    def class_decorator(cls):
        SingleCommandFactory.registered_commands[command_name] = cls
        return cls

    return class_decorator


@_register_single_command('echo')
class CommandEcho(SingleCommand):
    pass


@_register_single_command('wc')
class CommandWc(SingleCommand):
    pass


@_register_single_command('cat')
class CommandCat(SingleCommand):
    pass


@_register_single_command('pwd')
class CommandPwd(SingleCommand):
    pass


@_register_single_command('exit')
class CommandExit(SingleCommand):
    pass


@_register_single_command('cd')
class CommandCd(SingleCommand):
    pass
