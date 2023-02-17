import os
from omnisynth.value_converter import ValueConverter
from omnisynth.osc_message_sender import OscMessageSender


class Patch:
    def __init__(self, filename):
        self.filename = filename
        self.name = filename.split('/')[-1].split('.')[0]
        self.params = dict()
        self.compiled = False

    def compile(self):
        """
        Compiles this patch via OSC, if it has not already been compiled.
        """
        # return if already compiled
        if self.compiled:
            return

        print(f'Compiling patch {self.filename}...')
        # compile patch
        OscMessageSender.send_omni_message('compile', self.filename)

        self.compiled = True

    def get_interpolated_param_value(self, param_name):
        """
        Retrieve the real MIDI value of the given parameter for this patch

        Args:
            param_name (String): the parameter name

        Returns:
            Number: the real MIDI value of the parameter
        """
        return ValueConverter.converted_value(param_name, self.params[param_name])

    def set_param_initial_value(self, param_name, param_value):
        """
        Adds the parameter to this patch if not already added, and sets the value to the given value.

        Args:
            param_name (_type_): _description_
            param_value (_type_): _description_
        """
        self.params[param_name] = param_value

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
        return isinstance(obj, Patch) and obj.filename == self.filename
