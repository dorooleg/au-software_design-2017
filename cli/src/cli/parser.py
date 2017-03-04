"""A module with Parser responsibility.

Parsing is one of the later steps in
program compilation or intepreting.

It ensures that the stream of lexems
form a valid program. The result
is a tree that represents a program.

In our case, the result will be
:class:`commands.RunnableCommand`.
"""
from cli.commands import CommandChainPipe, CommandAssignment
from cli.single_command import SingleCommandFactory
from cli.exceptions import ParseException
from cli.lexer import LexemType


class Parser:
    """A static class for parsing a list of lexems.

    Parser ensures that a stream of lexems
    match a syntactic structure of a valid command.
    It also builds a representation of this
    command alongway.
    """

    @staticmethod
    def build_command(lexems):
        """Build :class:`commands.RunnableCommand` out of list of lexems.

        Our grammar is as following::

            <start> ::= <command> (PIPE <command>)*
            <command> ::= <assignment> | <single_command>
            <assignment> ::= ASSIGNMENT
            <single_command> ::= STRING (STRING | QUOTED_STRING | ASSIGNMENT)*

        where ASSIGNMENT, QUOTED_STRING, STRING and PIPE are lexems.

        Every rule is implemented as a static method with name _parse_`smth`.
        It returns a pair:

            - a resulting :class:`commands.RunnableCommand`
            - a list of unparsed lexems
        """
        runnable, unparsed_lexems = Parser._parse_start(lexems)

        if unparsed_lexems:
            raise ParseException('Not all lexems were parsed. The first starts '\
                                 'at {}'.format(unparsed_lexems[0].get_position()))

        return runnable

    @staticmethod
    def _consume_one_lexem(lexem_list, desired_lexem_type):
        """Consume a lexem of the desired type. Return list of lexems without consumed one.

        Raises:
            ParseException, if the list is empty or the first lexem is not
                of a type `desired_lexem_type`.
        """
        if not lexem_list:
            raise ParseException('Expected lexem of type {}, found ' \
                                 'none.'.format(desired_lexem_type.name))

        if lexem_list[0].get_type() != desired_lexem_type:
            raise ParseException('Expected lexem of type {}, found '\
                                 'lexem of type {}.'.format(desired_lexem_type.name,
                                                            lexem_list[0].get_type().name))

        return lexem_list[1:]

    @staticmethod
    def _parse_start(lexems):
        first_command, unparsed_lexems = Parser._parse_command(lexems)

        result_command = first_command
        while unparsed_lexems:
            unparsed_lexems = Parser._consume_one_lexem(unparsed_lexems, LexemType.PIPE)
            current_command, unparsed_lexems = Parser._parse_command(unparsed_lexems)

            result_command = CommandChainPipe(result_command, current_command)

        return result_command, unparsed_lexems

    @staticmethod
    def _parse_command(lexems):
        try:
            return Parser._parse_assignment(lexems)
        except ParseException:
            pass

        return Parser._parse_single_command(lexems)


    @staticmethod
    def _parse_assignment(lexems):
        unprocessed_lexems = Parser._consume_one_lexem(lexems, LexemType.ASSIGNMENT)
        command = CommandAssignment([lexems[0].get_value()])
        return command, unprocessed_lexems

    @staticmethod
    def _parse_single_command(lexems):
        rest_lexems = Parser._consume_one_lexem(lexems, LexemType.STRING)

        cmd_name_and_args = [lexems[0]]
        while rest_lexems:
            first_lex_type = rest_lexems[0].get_type()

            if first_lex_type in (LexemType.QUOTED_STRING, LexemType.STRING,
                                  LexemType.ASSIGNMENT):
                cmd_name_and_args.append(rest_lexems[0])
                rest_lexems = Parser._consume_one_lexem(rest_lexems, first_lex_type)
            else:
                break

        command = SingleCommandFactory.build_command(cmd_name_and_args)
        return command, rest_lexems
