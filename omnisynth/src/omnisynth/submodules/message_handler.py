class MessageHandler:
    """
    Handles incoming messages with arguments
    """

    def __init__(self):
        self.callbacks = dict()

    def attach_message_listener(self, message_name, callback):
        self.callbacks[message_name] = callback

    def handle_message(self, command_name, *command_args):
        """
        Processes the message given to this MessageHandler

        command_name : str
            the name of the command, such as /noteOff
        command_args : arr[str]
            the command arguments
        """

        if command_name in self.callbacks:
            self.callbacks[command_name](command_args)
        else:
            print(f'Message received with no listener: ${message_name}')
