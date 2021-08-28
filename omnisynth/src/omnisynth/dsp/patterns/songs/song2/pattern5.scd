/*
desc: Simple 4/4 quarter note kick drum at 120 bpm.
author: Omar Barazanji
date: 5/27/2021
*/

~bpm = (60/120)*4;
a = Scale.melodicMinor;


Pdef (
	\pattern5,
	Pbind(
		\instrument, \tone2,
		\bend, ~bend.linlin(0,16383,-2,2),
		\scale, a,
		\degree, Pseq((0..3), inf),
		\root, Pexprand(-90,-50),
		\out, 0,
		\amp, Pexprand(0.05, 0.07, inf),
		\gate, 1,
		\mod_freq, 0,
		\mod_amp, 30,
		\lpf_cutoff, 20000, 
		\hpf_cutoff, 20,
		\attack_time, Pexprand(0.01, 0.03, inf), 
		\decay_time, 0.1, 
		\sustain, 0.1,
		\release_time, 1.0,
		\bias, 0.0,
		\lin_start, 600, 
		\lin_stop, 2,
		\lin_duration, 1.0,
		\dur, Pseq([1/1], inf),
		\stretch, ~bpm,
	);
).quant_(~bpm);