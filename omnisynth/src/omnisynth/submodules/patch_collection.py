import os
from .osc_message_sender import OscMessageSender
from .patch import Patch


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

    def contains_patch(self, filename):
        """
        Returns true if this PatchCollection contains a patch with the given filename,
        and false otherwise

        Args:
            filename (str): the filename of the patch

        Returns:
            bool: true if this PatchCollection contains a patch with the given filename,
                  false otherwise
        """

        for patch in self.patches:
            if patch.filename == filename:
                return True
        return False

    def patch_count(self):
        return len(patches)
