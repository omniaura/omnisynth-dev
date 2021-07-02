/*
desc: Read midi.
author: Omar Barazanji
date: 5/27/2021
*/

~bpm = (60/120)*4;
a = Scale.minor;

// m = SimpleMIDIFile.read("C:/Users/ozanj/Desktop/Code/omnisynth/dsp/patterns/midi/birds.mid");

// m.p(\tone1).play;

/*
High Hats.
*/
Pdef (
	\pattern6,
	Pbind(
		\instrument, \tone7,
		\scale, a,
		\degree, Pseq(([1]), inf), 
		\root, 20,
		\out, 0,
		\amp, Pexprand(0.08, 0.1, inf),
		\gate, 1,
		\mod_freq, Pexprand(5000, 6000, inf),
		\mod_amp, 300,
		\lpf_cutoff, 20000, 
		\hpf_cutoff, 8000,
		\attack_time, Pexprand(0.01, 0.02, inf), 
		\decay_time, 0.06, 
		\sustain, 0.02,
		\release_time, 0.01,
		\lin_start, 19000, 
		\lin_stop, 17000,
		\lin_duration, 0.05,
		\bias, 0.0,
		\dur, Prand([
            Pseq([1/8], 8),
            Pseq([1/32], 8),
            Pseq([1/12], 6),
            ], inf),
		\stretch, ~bpm,
	);
).quant_(~bpm);