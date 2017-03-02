class Preprocessor:
    """A static class for preprocessing a shell input string.

    Given a raw string, we want to preprocess it, i.e.
    substitue things like `$x` into previously
    assigned value of `x`.
    """

    @staticmethod
    def substitute_environment_variables(raw_str, env):
        """Do a one-time pass over string and substitute `$x`-like patterns.

        Args:
            raw_str (str): an initial, unprocessed string;
            env (:class:`environment.Environment`): an environment
                in which this string must be expanded.

        Returns:
            str. The processed string.
            All substrings in single quotes are left untouched.

            Inside double quotes, things starting with `$` sign and
            ending in 
                - space symbol 
                - end-of-string
                - `$` sign
            are treated as variable names. The values for these
            variables are queried from the input `env`.

            Outside any quotation, similar rules apply: things
            that start with `$` and end either
                - before the next space character
                - before the other `$` sign
                - at the end of the input string
                - at the beginning of quotes (single or double) 
            are treated as variable names.

        Example:
            If the environment contains
                x=1
                long_name=qwe
            Then the following substitutions apply (nonexistant variables
            are substituted by an empty string):
                echo "123$x"    -->     echo "1231"
                echo "123$x "    -->     echo "1231 "
                echo "123$xy "    -->     echo "123 "
                echo "123$x dfg"    -->     echo "1231 dfg"
                echo $long_name'123'  -->   echo qwe'123'
                echo $long_name2'123'  -->   echo '123'
                echo $x '123'  -->   echo 1 '123'
                echo $x"qwe"    -->   echo 1"qwe"
                echo $x$long_name  -->  echo 1qwe
                echo `$x`"$x"  -->  echo `$x`"1"
        """
        pass
