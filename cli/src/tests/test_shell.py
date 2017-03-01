import unittest
from cli import shell
from cli import exceptions

import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ShellTest(unittest.TestCase):
    """System testing: invoking full shell commands.
    """

    def setUp(self):
        self.shell = shell.Shell() 

    def tearDown():
        pass

    @unittest.expectedFailure
    def test_var_expansion(self):
        """Test that string expansion (single and double quotes) works well.
        """
        command_result = self.shell.process_input('x=qwe')
        self.shell.apply_command_result(command_result)
        self.assertEqual(command_result.get_return_code(), 0)

        command_result = self.shell.process_input("""echo '123$x' "45$x" """)
        self.assertEqual(command_result.get_output(), '123$x 45asb')
        self.assertEqual(command_result.get_return_code(), 0)

        command_result = self.shell.process_input("""echo $x""")
        self.assertEqual(command_result.get_output(), 'asb')
        self.assertEqual(command_result.get_return_code(), 0)

        command_result = self.shell.process_input("""echo "45$x " """)
        self.assertEqual(command_result.get_output(), '45asb')
        self.assertEqual(command_result.get_return_code(), 0)

        command_result = self.shell.process_input("""echo "45$x bla" """)
        self.assertEqual(command_result.get_output(), '45asb bla')
        self.assertEqual(command_result.get_return_code(), 0)

        command_result = self.shell.process_input("""echo "45$xbla" """)
        self.assertEqual(command_result.get_output(), '45')
        self.assertEqual(command_result.get_return_code(), 0)

    @unittest.expectedFailure
    def test_cat_wc(self):
        """A simple piped command: cd; cat smth | wc
        """
        command_result = self.shell.process_input('cd {}'.format(BASE_DIR))
        command_result = self.shell.process_input('cat wc_file.txt | wc')
        self.assertEqual(command_result.get_output(), '      2       6      24')


    @unittest.expectedFailure
    def test_cd_pwd(self):
        """A simple script execution: cd; pwd.
        """
        command_result = self.shell.process_input('cd {}'.format(BASE_DIR))
        command_result = self.shell.process_input('pwd')
        self.assertEqual(command_result.get_output(), BASE_DIR)
