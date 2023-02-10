import os
from .osc_message_sender import OscMessageSender


class Pattern:
    def __init__(self, filename):
        self.filename = filename
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
            self.filename, "setPatternState", 'start')

    def stop(self):
        if not self.compiled:
            self.compile()

        self.playing = False
        OscMessageSender.send_client_message(
            self.filename, "setPatternState", 'stop')

    def __eq__(self, obj):
        return isinstance(obj, Pattern) and obj.filename == self.filename
