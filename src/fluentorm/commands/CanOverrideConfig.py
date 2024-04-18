from cleo.commands.command import Command
from cleo.io.inputs.option import Option


class CanOverrideConfig(Command):
    def __init__(self):
        super().__init__()
        self.add_option()

    def add_option(self):
        self._definition.add_option(
            Option(
                name="config",
                shortcut="C",
                description="The path to the ORM configuration file. If not given DB_CONFIG_PATH env variable will be used and finally 'config.database'."
            )
        )
