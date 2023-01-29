class OscMessageSender:
    def send_message(command, control, *args):
        if command == "server":
            port = OSC_SERVER_CONTROL_PORT
        else:
            port = OSC_CLIENT_CONTROL_PORT

        tx = argparse.ArgumentParser()
        tx.add_argument("--ip", default="127.0.0.1", help="osc default ip")
        tx.add_argument("--port", type=int, default=port,
                        help="supercollider rx osc port")
        tx_args = tx.parse_args()
        client = udp_client.SimpleUDPClient(tx_args.ip, tx_args.port)

        if command == "server":
            client.send_message(control, args[0])
        else:
            control_block = [control]
            for x in args:
                control_block.append(x)
            message = (command, control_block)
            client.send_message(command, control_block)
