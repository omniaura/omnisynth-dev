# Used for sending via OSC
from pythonosc import udp_client
import argparse

OSC_SERVER_PORT = 57110
OSC_CLIENT_PORT = 57120

server_tx = argparse.ArgumentParser()
server_tx.add_argument("--ip", default="127.0.0.1", help="osc default ip")
server_tx.add_argument("--port", type=int, default=OSC_SERVER_PORT,
                       help="supercollider rx osc port")
server_tx_args = server_tx.parse_args()
OSC_SERVER_UDP_CLIENT = udp_client.SimpleUDPClient(
    server_tx_args.ip, server_tx_args.port)

client_tx = argparse.ArgumentParser()
client_tx.add_argument("--ip", default="127.0.0.1", help="osc default ip")
client_tx.add_argument("--port", type=int, default=OSC_CLIENT_PORT,
                       help="supercollider rx osc port")
client_tx_args = client_tx.parse_args()
OSC_CLIENT_UDP_CLIENT = udp_client.SimpleUDPClient(
    client_tx_args.ip, client_tx_args.port)


class OscMessageSender:
    def send_server_message(msg, msgArg):
        OSC_SERVER_CLIENT.send_message(msg, msgArg)

    def send_client_message(command, msg, *msgArgs):
        control_block = [msg]
        for x in msgArgs:
            control_block.append(x)
        print(f'Command: {command}')
        print(f'Control block: {control_block}')
        OSC_CLIENT_UDP_CLIENT.send_message(command, control_block)

    # def send_message(command, control, *args):
    #     if command == "server":
    #         client.send_message(control, args[0])
    #     else:
    #         control_block = [control]
    #         for x in args:
    #             control_block.append(x)
    #         message = (command, control_block)
    #         client.send_message(command, control_block)

    def send_omni_message(msg, *msgArgs):
        OscMessageSender.send_client_message('/omni', msg, *msgArgs)
