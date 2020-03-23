from cx_Freeze import Executable, setup

executables = [Executable("main.py", base=None)]

packages = ["idna", "random", "sys", "os", "itertools"]
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "Подземелье Опасностей",
    options = options,
    version = "0.0.2",
    description = 'game second build.',
    executables = executables
)