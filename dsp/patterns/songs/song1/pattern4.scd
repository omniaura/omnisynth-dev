/*
desc: Simple 4/4 kick drum at 120 bpm.
author: Omar Barazanji
date: 5/27/2021
*/

~bpm = (60/120)*4;
a = Scale.melodicMinor;


Pdef (
	\pattern4,
	Pbind(
		\instrument, \tone5,
		\bend, ~bend.linlin(0,16383,-2,2),
		\scale, a,
		\degree, Pseq((0..3), inf),
		\root, -20,
		\out, 0,
		\amp, Pexprand(0.02, 0.05, inf),
		\gate, 1,
		\mod_freq, 2000,
		\mod_amp, 300,
		\lpf_cutoff, 20000, 
		\hpf_cutoff, 100,
		\attack_time, Pexprand(0.01, 0.03, inf), 
		\decay_time, 0.1, 
		\sustain, 0.1,
		\release_time, 0.1,
		\bias, 0.0,
		\lin_start, 500, 
		\lin_stop, 1,
		\lin_duration, 0.2,
		\dur, Pseq([1/8, Rest(1/16), 1/16, 1/8, 1/8, 1/16, 1/8, Rest(1/16)], inf),
		\stretch, ~bpm,
	);
).quant_(~bpm);