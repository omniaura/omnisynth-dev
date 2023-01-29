import os
from submodules.value_converter import ValueConverter
from submodules.osc_message_sender import OscMessageSender


class Patch:
    def __init__(self, filename):
        self.filename = filename
        self.params = dict()
        self.compiled = False

    def compile(self):
        """
        Compiles this patch via OSC, if it has not already been compiled.
        """
        # return if already compiled
        if self.compiled:
            return

        # compile patch
        OscMessageSender.send_omni_message('compile', self.filename)

        self.compiled = True

    def get_param_value(self, param_name):
        """
        Retrieve the value of the given parameter for this patch

        Args:
            param_name (String): the parameter name

        Returns:
            Number: the value of the parameter
        """
        return self.params[param_name]

    def get_param_real_value(self, param_name):
        """
        Retrieve the real MIDI value of the given parameter for this patch

        Args:
            param_name (String): the parameter name

        Returns:
            Number: the real MIDI value of the parameter
        """
        return ValueConverter.converted_value(param_name, self.params[param_name])

    def set_param_value(self, param_name, param_value):
        if not self.compiled:
            self.compile()

        self.params[param_name] = param_value
        real_value = self.get_param_real_value(param_name)
        OscMessageSender.send_message(
            f"/{self.filename}", "setParam", param_name, real_value)
