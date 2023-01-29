from pythonosc import dispatcher


class OscMessageHandler:
    """
    Handles incoming messages with arguments
    """

    def __init__(self):
        self.callbacks = dict()
        self.osc_dispatcher = dispatcher.Dispatcher()

    def attach_message_listener(self, message_name, callback):
        if message_name in callbacks:
            return

        self.callbacks[message_name] = callback
        self.osc_dispatcher.map(message_name, handle_message)

    def handle_message(self, *msgArgs):
        """
        Processes the message given to this MessageHandler

        command_name : str
            the name of the command, such as /noteOff
        command_args : arr[str]
            the command arguments
        """

        command_name = args[0]
        command_args = args[1:]

        if command_name in self.callbacks:
            self.callbacks[command_name](command_args)
        else:
            print(f'Message received with no listener: ${message_name}')
