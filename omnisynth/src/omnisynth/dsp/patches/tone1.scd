/*
desc: Default patch.
author: Omar Barazanji
date: 11/11/20
*/

~bend = 8193;
~notes = Array.newClear(128);
~synth = "tone1";
~lpf_cutoff = 20000;
~hpf_cutoff = 20;
~attack_time = 0.01;
~decay_time = 0.3;
~sustain = 0.5;
~release_time = 1.0;

o = OSCFunc({

	// arguments to OSCFunc.
	| msg, time, addr, recvPort |
	var temp;
	// post all messages to terminal window.
	[msg, time, addr, recvPort].postln;

	case

		// Parameter adjustment.
		{msg[1] == "filterSel".asSymbol} {
			if (msg[2] == "lpf".asSymbol) {
				~lpf_cutoff = msg[3].asFloat;
			};
			if (msg[2] == "hpf".asSymbol) {
				~hpf_cutoff = msg[3].asFloat;
			};
			if (msg[2] == "attack".asSymbol) {
				~attack_time = msg[3].asFloat;
			};
			if (msg[2] == "decay".asSymbol) {
				~decay_time = msg[3].asFloat;
			};
			if (msg[2] == "sustain".asSymbol) {
				~sustain = msg[3].asFloat;
			};
			if (msg[2] == "release".asSymbol) {
				~release_time = msg[3].asFloat;
			};
		}

		// base case - set synth to default patch.
		{true} {~synth = ~synth};

}, '/tone1').add;

/*
Synth function.
*/
SynthDef.new(\tone1, {
	arg freq=440, amp=0.6, gate=1, out=0, bend=0,
		lpf_cutoff=20000, hpf_cutoff=20, attack_time=0.01,
		decay_time=0.3, sustain=0.5, release_time=1.0, bias=0.0;


	var sig, sig1, sig2, raw_sig, filter_sig, env;

	/*
	signal creation section.
	*/
	sig1 = LFTri.ar([freq*bend.midiratio, 0]);
	sig2 = SinOsc.ar([0, (freq*2)*bend.midiratio]);
    raw_sig = sig1 + sig2;

	/*
	Envelope section.
	*/
	env = EnvGen.kr(Env.adsr(
		attack_time,decay_time,sustain,
		release_time, -4, bias), gate, doneAction:2);

	/*
	Filter section.
	*/
	filter_sig = LPF.ar(raw_sig, lpf_cutoff);
	filter_sig = HPF.ar(filter_sig, hpf_cutoff);

	/*
	Combining all components.
	*/
	sig = filter_sig * env * amp !2;
	sig = Splay.ar(sig);

	Out.ar(out, sig);
}).add;

/*
Note on function.
*/
MIDIdef.noteOn(\noteOnDef, {
	arg vel, nn, chan, src;
	var temp;
	[vel, nn].postln;
	"tone1?".postln;
	n.sendMsg("/noteOn",nn,vel);
	~notes[nn] = Synth.new(
		~synth,
		[
			\freq, nn.midicps,
			\amp, vel.linexp(1,127,0.01,0.03),
			\gate, 1,
			\bend, ~bend.linlin(0,16383,-2,2),
			\lpf_cutoff, ~lpf_cutoff,
			\hpf_cutoff, ~hpf_cutoff,
			\attack_time, ~attack_time,
			\decay_time, ~decay_time,
			\sustain, ~sustain,
			\release_time, ~release_time,
		]
	);
});

/*
Note off function.
*/
MIDIdef.noteOff(\noteOffDef, {
	arg vel, nn;
	var temp;
	[vel, nn].postln;
	n.sendMsg("/noteOff",nn,vel);
	~notes[nn].set(\gate, 0);
	~notes[nn] = nil;
});

/*
Pitch wheel function.
*/
MIDIdef.bend(\bendDef, {
	arg val, chan;
	[val, chan].postln;
	~bend = val;
	~notes.do{arg synth; synth.set(\bend, val.linlin(0,16383, -2, 2))};
}, chan:0);

MIDIdef.cc(\controlDef, {
	arg val, src, chan;
	[val, src, chan].postln;
	n.sendMsg("/control",val, src, chan);
});

