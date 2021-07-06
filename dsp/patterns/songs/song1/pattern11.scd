~bpm = (60/120)*4;
a = Scale.melodicMinor;

Pdef (
	\pattern11,
	Pbind(
		\instrument, \tone8,
		\scale, a,
		\degree, Pseq((4..3)++(1..0) ,inf),
		\root, -16,
		\out, 0,
		\amp, Pexprand(0.03, 0.2, inf),
		\gate, 1,
		\mod_freq, Pwhite(102, 106, inf),
		\lpf_cutoff, 1200, 
		\hpf_cutoff, 900,
		\attack_time, Pexprand(0.07, 0.09, inf), 
		\decay_time, 0.3, 
		\sustain, 0.4,
		\release_time, 2.2,
		\lin_duration, 2.0,
		\bias, 0.0,
		\dur, Pseq([1/1], inf),
		\stretch, ~bpm,
	);
).quant_(~bpm);