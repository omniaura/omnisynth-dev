import os
from omnisynth.osc_message_sender import OscMessageSender
from omnisynth.pattern import Pattern


class PatternCollection:
    def __init__(self):
        self.patterns = []

    def find_or_add_pattern(self, pattern_filename):
        for pattern in self.patterns:
            if pattern.filename == pattern_filename:
                return pattern
        pattern = Pattern(patch_filename)
        pattern.compile()
        self.patterns.append(pattern)
        return pattern

    def pattern_count(self):
        return len(patches)
