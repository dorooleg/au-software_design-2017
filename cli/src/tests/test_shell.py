import unittest
import os.path

from cli import shell
from cli import exceptions


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ShellTest(unittest.TestCase):
    """System testing: invoking full shell commands.
    """

    def setUp(self):
        self.shell = shell.Shell() 

    def tearDown(self):
        pass

    @unittest.expectedFailure
    def test_sample_from_presentation(self):
        """A test from hwproj presentation.

        >echo "Hello, world!"
        Hello, world!
        > FILE=example.txt
        > cat $FILE
        Some example text
        > cat example.txt | wc
        1 3 18
        > echo 123 | wc
        1 1 3
        """
        command_result = self.shell.process_input('echo "Hello, world!"')
        self.assertEqual(command_result.get_output(), 
                'Hello, world!')
        self.assertEqual(command_result.get_return_code(), 0)

        command_result = self.shell.process_input('FILE=example.txt')
        self.assertEqual(command_result.get_output(), '')
        self.assertEqual(command_result.get_return_code(), 0)

        command_result = self.shell.process_input('cat $FILE')
        self.assertEqual(command_result.get_output(), 'Some example text')
        self.assertEqual(command_result.get_return_code(), 0)

        command_result = self.shell.process_input('cat example.txt | wc')
        self.assertEqual(command_result.get_output(), '1 3 18')
        self.assertEqual(command_result.get_return_code(), 0)

        command_result = self.shell.process_input('echo 123 | wc')
        self.assertEqual(command_result.get_output(), '1 1 3')
        self.assertEqual(command_result.get_return_code(), 0)

    @unittest.expectedFailure
    def test_subst_exit(self):
        """Test that string expansion works for substituting commands.
        """
        command_result = self.shell.process_input('x=exit')
        self.assertRaises(exceptions.ExitException,
                self.shell.process_input, '$x')


    @unittest.expectedFailure
    def test_cat_wc(self):
        """A simple piped command: cd; cat smth | wc
        """
        command_result = self.shell.process_input('cd {}'.format(BASE_DIR))
        command_result = self.shell.process_input('cat wc_file.txt | wc')
        self.assertEqual(command_result.get_output(), '2 6 24')


    @unittest.expectedFailure
    def test_cd_pwd(self):
        """A simple script execution: cd; pwd.
        """
        command_result = self.shell.process_input('cd {}'.format(BASE_DIR))
        command_result = self.shell.process_input('pwd')
        self.assertEqual(command_result.get_output(), BASE_DIR)
