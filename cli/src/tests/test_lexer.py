import unittest

from cli.exceptions import LexException
from cli.lexer import Lexer, LexemType, Lexem


class LexerTest(unittest.TestCase):
    """Tests for checking lexing correctness.
    """

    def test_invalid_quotes(self):
        self.assertRaises(LexException, Lexer.get_lexems,
                '"xyz')
        self.assertRaises(LexException, Lexer.get_lexems,
                "xyz'")

    def test_quotes_without_space(self):
        lex_result = Lexer.get_lexems('"xy"\'qwe\'')
        self.assertEqual(len(lex_result), 2)
        self.assertEqual(lex_result[0].get_type(), LexemType.QUOTED_STRING)
        self.assertEqual(lex_result[1].get_type(), LexemType.QUOTED_STRING)

    def test_many_whitespaces(self):
        lex_result = Lexer.get_lexems('echo      hello        "maybe"   ')
        self.assertEqual(len(lex_result), 3)
        self.assertEqual(lex_result[0].get_type(), LexemType.STRING)
        self.assertEqual(lex_result[0].get_value(), 'echo')
        self.assertEqual(lex_result[1].get_type(), LexemType.STRING)
        self.assertEqual(lex_result[1].get_value(), 'hello')
        self.assertEqual(lex_result[2].get_type(), LexemType.QUOTED_STRING)
        self.assertEqual(lex_result[2].get_value(), 'maybe')

    def test_positions(self):
        lex_result = Lexer.get_lexems('cat  file.txt')
        self.assertEqual(len(lex_result), 2)
        self.assertEqual(lex_result[0].get_position(), '(0:2)')
        self.assertEqual(lex_result[1].get_position(), '(5:12)')

    def test_assignment(self):
        lex_result = Lexer.get_lexems('x a=b')
        self.assertEqual(len(lex_result), 2)
        self.assertEqual(lex_result[1].get_type(), LexemType.ASSIGNMENT)
        self.assertEqual(lex_result[1].get_value(), 'a=b')

    def test_pipe(self):
        lex_result = Lexer.get_lexems('pwd | wc')
        self.assertEqual(len(lex_result), 3)
        self.assertEqual(lex_result[0].get_type(), LexemType.STRING)
        self.assertEqual(lex_result[1].get_type(), LexemType.PIPE)
        self.assertEqual(lex_result[2].get_type(), LexemType.STRING)
