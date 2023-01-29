FILTER_PARAMS = ['lpf', 'hpf']
ADSR_PARAMS = ['attack', 'decay', 'sustain', 'release']
LIN_PARAMS = ['lin_start', 'lin_stop']
DURATION_PARAMS = ['lin_duration']


class ValueConverter:
    """
    Converts a parameter value given its name to its real value used for audio / light processing

    """
    def converted_value(param_name, param_value):
        if self.param_name in FILTER_PARAMS:
            return self.__to_freq()
        if self.param_name in ADSR_PARAMS:
            return self.__to_adsr()
        if self.param_name in LIN_PARAMS:
            return self.__to_lin()
        if self.param_name in DURATION_PARAMS:
            return self.__to_duration()
        return 0

    def __to_freq(val):
        return np.linspace(20, 20000, 128).tolist()[val]

    def __to_adsr(val):
        return np.linspace(0.001, 2, 128).tolist()[val]

    def __to_lin(val):
        return np.linspace(1, 3000, 128).tolist()[val]

    def __to_duration(val):
        return np.linspace(0.001, 5, 128).tolist()[val]
