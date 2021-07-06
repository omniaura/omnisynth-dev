~bpm = (60/120)*4;
a = Scale.melodicMinor;

Pdef (
	\pattern7,
	Pbind(
		\instrument, \tone3,
		\scale, a,
		\bend, ~bend.linlin(0,16383,-2,2),
		\degree, Pseq((4..3)++(1..0) ,inf),
		\root, 3,
		\out, 0,
		\amp, Pexprand(0.08, 0.15, inf),
		\gate, 1,
		\mod_freq, Pwhite(102, 106, inf),
		\lpf_cutoff, 20000, 
		\hpf_cutoff, 20,
		\attack_time, Pexprand(0.07, 0.09, inf), 
		\decay_time, 0.3, 
		\sustain, 0.4,
		\release_time, 2.2,
		\lin_start, 100, 
		\lin_stop, 600,
		\lin_duration, 5.0,
		\bias, 0.0,
		\dur, Pseq([1/1], inf),
		\stretch, ~bpm,
	);
).quant_(~bpm);

