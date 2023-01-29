import os
from submodules.value_converter import ValueConverter
from submodules.osc_message_sender import OscMessageSender


class Patch:
    def __init__(self, filename):
        self.filename = filename
        self.params = dict()
        self.compiled = False

    def compile(self):
        command = "/omni"
        control = "compile"
        OscMessageSender.send_message(command, control, filename)
        self.compiled = True

    def get_param_value(self, param_name):
        return self.params[param_name]

    def get_param_real_value(self, param_name):
        return ValueConverter.converted_value(param_name, self.params[param_name])

    def set_param_value(self, param_name, param_value):
        if not self.compiled:
            self.compile()

        self.params[param_name] = param_value
        real_value = ValueConverter.converted_value(param_name, param_value)
        command = f"/{self.filename}"
        control = "setParam"
        OscMessageSender.send_message(
            command, control, param_name, real_value)
