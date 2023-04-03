import numpy as np

FREQ_PARAMS = ['lpf', 'hpf']
ADSR_PARAMS = ['attack', 'decay', 'sustain', 'release']
LIN_PARAMS = ['lin_start', 'lin_stop']
DURATION_PARAMS = ['lin_duration']
MOD_PARAMS = ['mod_freq']

FREQ_VALUES = np.linspace(20, 20000, 128)
ADSR_VALUES = np.linspace(0.001, 2, 128)
LIN_VALUES = np.linspace(1, 3000, 128)
DURATION_VALUES = np.linspace(0.001, 5, 128)
MOD_VALUES = np.linspace(0, 5000, 128)


class ValueConverter:
    def to_normalized_value(param_name, midi_value):
        """
        Converts a midi_value (0-127) value to a normalized value based on the param name

        Args:
            param_name (str): the name of the parameter
            midi_value (int): a number between 0 and 127

        Returns:
            float: the midi value of the param
        """
        if param_name in FREQ_PARAMS:
            return FREQ_VALUES[midi_value]
        if param_name in ADSR_PARAMS:
            return ADSR_VALUES[midi_value]
        if param_name in LIN_PARAMS:
            return LIN_VALUES[midi_value]
        if param_name in DURATION_PARAMS:
            return DURATION_VALUES[midi_value]
        if param_name in MOD_PARAMS:
            return MOD_VALUES[midi_value]
        return 0

    def to_midi_value(param_name, normalized_value):
        """
        Converts a normalized_value value to a midi value between 0 and 127

        Args:
            param_name (str): the name of the parameter
            normalized_value (float): the midi value

        Returns:
            float: the value of the param normalized between 0 and 127
        """
        if param_name in FREQ_PARAMS:
            diff_arr = FREQ_VALUES - normalized_value
            return diff_arr.argmin()
        if param_name in ADSR_PARAMS:
            diff_arr = ADSR_VALUES - normalized_value
            return diff_arr.argmin()
        if param_name in LIN_PARAMS:
            diff_arr = LIN_VALUES - normalized_value
            return diff_arr.argmin()
        if param_name in DURATION_PARAMS:
            diff_arr = DURATION_VALUES - normalized_value
            return diff_arr.argmin()
        if param_name in MOD_PARAMS:
            diff_arr = MOD_VALUES - normalized_value
            return diff_arr.argmin()
        return 0
