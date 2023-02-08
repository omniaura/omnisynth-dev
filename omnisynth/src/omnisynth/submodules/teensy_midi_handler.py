'''
Handles sending commands to midi connections.

author: Omar Barazanji
date: 3/21/2021

Python: 3.7.x
'''

# used to package the serial data in midi format
import midi
import os
from midi import MidiConnector
from midi import Message, NoteOff, NoteOn


class TeensyMidiHandler:
    def __init__(self):
        print('Establishing Teensy MIDI connection...')
        self.midi_connection = 0
        if os.path.exists('/dev/ttyACM0'):
            # connection to the Teensy serial port
            self.midi_connection = MidiConnector('/dev/ttyACM0')
        elif os.path.exists('/dev/ttyACM1'):
            self.midi_connection = MidiConnector('/dev/ttyACM1')
        if self.midi_connection == 0:
            print('Could not establish Teensy MIDI connection! Exiting...')
        print('MIDI connection established.')

    def send_note(command, note, velocity):
        if self.midi_connection == 0:
            return

        msg = 0
        if command == "/noteOn":
            note_on = NoteOn(note, velocity)
            msg = Message(note_on, 2)
        elif command == "/noteOff":
            note_off = NoteOff(note, velocity)
            msg = Message(note_off, 2)

        if not msg == 0:
            self.midi_connection.conn.write(msg)
        else:
            print(f'Unexpected MIDI command received: ${command}')


if __name__ == "__main__":
    pass
