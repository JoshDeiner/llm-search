# monkeytype_config.py

from monkeytype.config import DefaultConfig

class Config(DefaultConfig):
    def repo_root(self):
        # Specify the root directory of your codebase
        return "."

    def python_version(self):
        # Specify the Python version if needed, like "3.10"
        return super().python_version()

# This line creates a CONFIG variable that MonkeyType expects
CONFIG = Config()
