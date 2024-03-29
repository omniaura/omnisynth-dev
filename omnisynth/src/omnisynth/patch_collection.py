import os
from omnisynth.patch import Patch


class PatchCollection:
    def __init__(self):
        self.patches = []

    def set_patch_param_internal_value(self, patch_filename, param_name, param_value):
        patch = self.find_or_add_patch(patch_filename)
        patch.params[param_name] = param_value

    def find_or_add_patch(self, patch_filename):
        """
        Finds or adds a patch to this PatchCollection, and compiles the patch if it was added.

        Args:
            patch_filename (String): the filename of the patch to add
        """

        for patch in self.patches:
            if patch.filename == patch_filename:
                return patch
        patch = Patch(patch_filename)
        patch.compile()
        self.patches.append(patch)
        return patch

    def find_patch_by_name(self, patch_name):
        return next(
            (patch for patch in self.patches if patch.name == patch_name), None)

    def patch_count(self):
        return len(self.patches)
