class OmniMessage:

    def __init__(self, command, *args):
        self.command = command
        self.args = args

    def build_from_args(args):

        for x in args:
            event.append(x)
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
