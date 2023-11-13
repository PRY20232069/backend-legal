class Mediator:
    def __init__(self):
        self.handlers = {}

    def register(self, command_type, handler):
        self.handlers[command_type] = handler

    def send(self, command):
        handler = self.handlers[type(command)]
        return handler.handle(command)