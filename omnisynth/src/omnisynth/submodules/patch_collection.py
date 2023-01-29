import os
from submodules.osc_message_sender import OscMessageSender
from submodules.patch import Patch


class PatchCollection:

    def __init__(self):
        self.patches = []
        self.active_patch = None

    def set_patch_param_value(self, patch_filename, param_name, param_value):
        """
        Set a patch parameter value. If a patch with the given filename has not yet been added and compiled,
        it will be before the value is set.

        Args:
            patch_filename (String): the filename of the patch
            param_name (String): the name of the patch parameter
            param_value (Number): the value to set the patch parameter to
        """

        patch = self.find_or_add_patch(patch_filename)
        patch.set_param_value(param_name, param_value)

    def set_active_patch(self, patch_filename):
        """
        Sets the patch with the given filename to the currently active patch. If the patch has not yet been added and compiled,
        it will be before being set active.

        Args:
            patch_filename (String): the filename of the patch to set active
        """
        patch = self.find_or_add_patch(patch_filename)

        directory = f"patches/{patch_filename}.scd"
        patch_path = os.path.abspath(directory).replace("\\", "/")
        OscMessageSender.send_omni_message(
            "selectPatch", patch_filename, patch_path)

        self.active_patch = patch

    def find_or_add_patch(self, patch_filename):
        """
        Finds or adds a patch to this PatchCollection, and compiles the patch if it was added.

        Args:
            patch_filename (String): the filename of the patch to add
        """

        for patch in self.patches:
            if patch.filename == filename:
                return patch
        patch = Patch(filename)
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
                return true
        return false