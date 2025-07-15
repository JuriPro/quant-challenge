from application.contracts import IMediator


class Mediator(IMediator):
    def __init__(self):
        self._command_handlers = {}
        self._query_handlers = {}

    def register_command_handler(self, command_type, handler):
        self._command_handlers[command_type] = handler

    def register_query_handler(self, query_type, handler):
        self._query_handlers[query_type] = handler

    # For Command
    async def send(self, command):
        handler = self._command_handlers.get(type(command))
        if handler:
            return await handler.handle(command)
        raise ValueError(f'No handler registered for command: {type(command).__name__}')

    # For Query
    async def query(self, query):
        handler = self._query_handlers.get(type(query))
        if handler:
            return await handler.handle(query)
        raise ValueError(f'No handler registered for query: {type(query).__name__}')
