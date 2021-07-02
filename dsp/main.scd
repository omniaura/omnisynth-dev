/*
desc: Main / top level for the Omnisynth.
author: Omar Barazanji
date: 1/16/21
*/

// boot server
s.boot;

Server.default.options.device = "ASIO : ASIO4ALL v2";

// Default patch
~synth = "tone1";

// Set freq to standard Hz
nil.set(\freq, 880);

// Grab any MIDI device plugged in.
MIDIClient.init;
MIDIIn.connectAll;

// Connection to OSC via localhost.
n = NetAddr.new("127.0.0.1", 7771);

// begin main
(

/* OSCFunc called when Python sends "/omni" a message.
 * This function will control the OmniSynth created in Python.
 */
o = OSCFunc( {

	// arguments to OSCFunc.
	| msg, time, addr, recvPort |
	var temp;
	// post all messages to terminal window.
	[msg, time, addr, recvPort].postln;

	case

		// Synth patch selector.
		{msg[1] == "synthSel".asSymbol} {
			~synth = msg[2].asString;
			MIDIdef.freeAll;
			msg[3].asString.load;
	        ~synth.postln;
		}

		// compiles all SynthDef's.
		{msg[1] == "compile".asSymbol} {
			msg[2].asString.load;
			MIDIdef.freeAll;
		}

		{msg[1] == "pdef_control".asSymbol} {
			if (msg[2] == "start".asSymbol) {
				Pdef(msg[4].asSymbol).play;
			};
			if (msg[2] == "compile".asSymbol) {
				msg[3].asString.load;
			};
		    if (msg[2] == "stop".asSymbol) {
			    Pdef(msg[4].asSymbol).stop;
			};
		}

		// base case - set synth to default patch.
		{true} {~synth = ~synth};

}, '/omni').add;


) // end main
