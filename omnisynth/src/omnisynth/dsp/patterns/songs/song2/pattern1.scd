/*
desc: Simple 4/4 quarter note kick drum at 120 bpm.
author: Omar Barazanji
date: 5/27/2021
*/

~bpm = (60/180)*4;
a = Scale.melodicMinor;


Pdef (
	\pattern1,
	Pbind(
		\instrument, \tone5,
		\scale, a,
		\bend, ~bend.linlin(0,16383,-2,2),
		\degree, Prand([[2,4,5], [6,8,7]], inf),
		\root, -10,
		\out, 0,
		\amp, Pexprand(0.03, 0.04, inf),
		\gate, 1,
		\mod_freq, Pwhite(50, 100, inf),
		\lpf_cutoff, 20000, 
		\hpf_cutoff, 20,
		\attack_time, Pexprand(0.01, 0.09, inf), 
		\decay_time, 0.3, 
		\sustain, 0.4,
		\release_time, 2.0,
		\lin_start, 100, 
		\lin_stop, 2,
		\lin_duration, 2.0,
		\bias, 0.0,
		\dur, Pseq([2], inf),
		\stretch, ~bpm,
	);
).quant_(~bpm);

