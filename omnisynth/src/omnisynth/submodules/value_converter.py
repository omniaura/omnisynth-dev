FILTER_PARAMS = ['lpf', 'hpf']
ADSR_PARAMS = ['attack', 'decay', 'sustain', 'release']
LIN_PARAMS = ['lin_start', 'lin_stop']
DURATION_PARAMS = ['lin_duration']


class ValueConverter:
    """
    Converts a parameter value given its name to its real value used for audio / light processing

    """

    def __init__(self, param_name, param_value):
        self.param_name = param_name
        self.param_value = param_value

    def converted_value(self):
        if self.param_name in FILTER_PARAMS:
            return self.__to_freq()
        if self.param_name in ADSR_PARAMS:
            return self.__to_adsr()
        if self.param_name in LIN_PARAMS:
            return self.__to_lin()
        if self.param_name in DURATION_PARAMS:
            return self.__to_duration()
        return 0

    def __to_freq(self):
        cc_to_freq = np.linspace(20, 20000, 128).tolist()
        return cc_to_freq[int(inp)]

    def __to_adsr(self):
        cc_to_adsr = np.linspace(0.001, 2, 128).tolist()
        return cc_to_adsr[int(inp)]

    def __to_lin(self):
        cp_to_lin = np.linspace(1, 3000, 128).tolist()
        return cp_to_lin[int(self.param_value)]

    def __to_duration(self):
        cp_to_duration = np.linspace(0.001, 5, 128).tolist()
        return cp_to_duration[int(self.param_value)]
