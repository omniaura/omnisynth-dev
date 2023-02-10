import os
from .osc_message_sender import OscMessageSender


class Pattern:
    def __init__(self, filename):
        self.filename = filename
        self.name = filename.split('/')[-1].split('.')[0]
        self.params = dict()
        self.playing = False
        self.compiled = False

    def compile(self):
        """
        Compiles this pattern via OSC, if it has not already been compiled.
        """
        # return if already compiled
        if self.compiled:
            return

        print(f'Compiling pattern {self.filename}...')
        # compile patch
        OscMessageSender.send_omni_message('compile', self.filename)

        self.compiled = True

    def start(self):
        if not self.compiled:
            self.compile()

        self.playing = True
        OscMessageSender.send_client_message(
            f"/{self.filename}", "setPatternState", 'start')

    def stop(self):
        if not self.compiled:
            self.compile()

        self.playing = False
        OscMessageSender.send_client_message(
            f"/{self.filename}", "setPatternState", 'stop')

    def sync_param(self, param_name, param_value):
        """
        Syncs a parameter with OSC by sending the 'setParam' message

        Args:
            param_name (_type_): _description_
            param_value (_type_): _description_
        """
        if not self.compiled:
            self.compile()

        self.params[param_name] = param_value
        OscMessageSender.send_client_message(
            f"/{self.filename}", "setParam", param_name, param_value)

    def __eq__(self, obj):
        return isinstance(obj, Pattern) and obj.filename == self.filename
