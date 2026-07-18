from model.Command_Type import CommandType
from model.Exceptions import UnknownCommand
class Dispatcher:
    def __init__(self):
        self.commands = {

        }

    async def handle(self, username: str, data: dict):
        command = data.get("type")
        if command is None:
            raise UnknownCommand()

        try:
            command = CommandType(command)
        except ValueError:
            raise UnknownCommand()

        handler = self.commands.get(command)
        if handler is None:
            raise UnknownCommand()

        await handler(username, data)
