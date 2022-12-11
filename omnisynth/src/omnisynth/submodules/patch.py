from .value_converter import ValueConverter


class Patch:
    def __init__(self, filename, osc_instance):
        self.filename = filename
        self.osc_instance = osc_instance

    def value_map(self, filt, inp):
        value = inp
        if filt == "lpf" or filt == "hpf":
            value = self.cc_to_freq[int(inp)]
        if filt == "attack" or filt == "decay" or filt == "sustain" or filt == "release":
            value = self.cc_to_adsr[int(inp)]
        if filt == "lin_start" or filt == "lin_stop":
            value = self.cc_to_lin[int(inp)]
        if filt == "lin_duration":
            value = self.cc_to_duration[int(inp)]
        return value

    def set_currently_active(self):
        directory = "patches/%s.scd" % self.filename
        command = "/omni"
        control = "patchSel"
        patch_path = os.path.abspath(directory).replace("\\", "/")
        self.osc_instance.transmit(command, control, self.filename, patch_path)

    def set_param_value(self, param_name, param_value):
        command = "/%s" % self.filename
        control = "paramSel"
        real_value = ValueConverter(param_name, param_value).converted_value()
        self.osc_instance.transmit(command, control, param_name, real_value)

    def get_param_value(self, param_name, osc_instance):
        command = "/%s" % self.filename
        control = "paramSel"
