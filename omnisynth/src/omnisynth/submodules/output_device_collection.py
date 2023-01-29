from submodules.output_device import OutputDevice
from submodules.osc_message_sender import OscMessageSender


class OutputDeviceCollection:
    def __init__(self):
        self.output_devices = []
        self.active_output_device = None

    def find_or_add_output_device(self, device_index, device_name):
        for device in self.output_devices:
            if device.name == device_name and device.index == device_index:
                return device

        device = OutputDevice(device_index, device_name)
        self.output_devices.append(device)
        return device

    def get_output_devices(self):
        return self.output_devices

    def set_active_output_device(self, device_index):
        output_device = next(
            (od for od in self.output_devices if od.index == device_index), None)

        if output_device is None:
            raise Exception(
                f"Output device with index {device_index} not found")

        self.active_output_device = output_device
        command = "/omni"
        control = "selectOutputDevice"
        OscMessageSender.send_message(
            command, control, output_device.device_name)
