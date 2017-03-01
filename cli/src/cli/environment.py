import pathlib 

class Environment:

    def __init__(self):
        pass

    def get_var(self, name: str) -> str:
        pass

    def set_var(self, name: std, value: str):
        pass

    def get_cwd(self) -> pathlib.Path:
        pass

    def set_cwd(self, dir_name: str):
        pass
