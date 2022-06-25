import os

# get omnisynth-dsp path
OMNISYNTH_PATH = os.getcwd().replace(
    'omnisynth-dev', 'omnisynth-dsp/').replace("\\", "/")

SUPERCOLLIDER_PROCESS_NAMES = ['sclang', 'scsynth']
