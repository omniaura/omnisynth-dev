class MessageHandler:
    """
    Handles incoming messages with arguments

    command_name : str
        the name of the command, such as /noteOff
    command_args : arr[str]
        the command arguments
    """

    def __init__(self, command_name, *command_args):
        self.command_name = command_name
        self.command_args = []
        for arg in command_args:
            self.command_args.append(arg)

    def handle_message(self):
        """
        Processes the message given to this MessageHandler
        """

        if command_name == "/noteOn" or command_name == "/noteOff":
            self.__handle_note_message()
        elif command_name == '/control':
            self.__handle_control_message()
        elif command_name == '/params':
            self.__handle_param_message()
        elif command_name == '/outDev':
            self.__handle_out_dev_message()
        elif command_name == '/server':
            self.__handle_server_message()

    def __handle_note_message(self):
        """
        Processes a /noteOn or /noteOff message
        """

        OmniMidi.send_note(self.command_name,
                           self.command_args[0], self.command_args[1])

    def __handle_control_message(self):
        """
        Processes a /control message
        """

    def __handle_param_message(self):
        """
        Processes a /params message
        """

        param = event
        synth = param[1]
        param_num = param[2]
        param_name = param[3]
        param_default_val = param[4]

        param_arr = {'params': {param_name: param_default_val}}
        key = synth
        if key in self.patch_param_table:
            if not str(param_arr['params']) in str(self.patch_param_table[key]['params']):
                self.patch_param_table[key]['params'][param_name] = param_default_val
                r.set('patchTable', json.dumps(self.patch_param_table))
        else:
            self.patch_param_table[key] = param_arr
            r.set('patchTable', json.dumps(self.patch_param_table))

        event = []
        for x in message_args:
            event.append(x)
        self.midi_evnt = event
        if event[0] == "/noteOn" or event[0] == "/noteOff":
            self.teensy.send_note(event)
        if event[0] == "/params":
            param = event
            synth = param[1]
            param_num = param[2]
            param_name = param[3]
            param_default_val = param[4]

            param_arr = {'params': {param_name: param_default_val}}
            key = synth
            if key in self.patch_param_table:
                if not str(param_arr['params']) in str(self.patch_param_table[key]['params']):
                    self.patch_param_table[key]['params'][param_name] = param_default_val
                    r.set('patchTable', json.dumps(self.patch_param_table))
            else:
                self.patch_param_table[key] = param_arr
                r.set('patchTable', json.dumps(self.patch_param_table))

        if event[0] == "/outDev":
            dev_num = event[1]
            dev_name = event[2]
            if dev_num not in self.out_dev_table:
                self.out_dev_table[dev_num] = dev_name
            r.set('outDevTable', json.dumps(self.out_dev_table))

        if event[0] == "/server":
            value = event[1]
            r.set("serverStatus", value)
