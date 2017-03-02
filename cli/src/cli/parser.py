"""A module with Parser responsibility.

Parsing is one of the later steps in
program compilation or intepreting.

It ensures that the stream of lexems
form a valid program. The result
is a tree that represents a program.

In our case, the result will be
:class:`commands.RunnableCommand`.
"""


class Parser:

    @staticmethod
    def build_command(lexems):
        pass
