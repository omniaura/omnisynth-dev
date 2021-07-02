~bpm = (60/180)*4;
a = Scale.melodicMinor;


/*
High Hats.
*/
Pdef (
	\pattern3,
	Pbind(
		\instrument, \tone7,
		\scale, a,
		\degree, Pseq(([1]), inf), 
		\root, 20,
		\out, 0,
		\amp, Pexprand(0.1, 0.12, inf),
		\gate, 1,
		\mod_freq, Pexprand(5000, 6000, inf),
		\mod_amp, 300,
		\lpf_cutoff, 20000, 
		\hpf_cutoff, 5000,
		\attack_time, Pexprand(0.01, 0.02, inf), 
		\decay_time, 0.06, 
		\sustain, 0.03,
		\release_time, 0.01,
		\lin_start, 19000, 
		\lin_stop, 17000,
		\lin_duration, 0.05,
		\bias, 0.0,
		\dur, Pseq([1/4], inf),
		\stretch, ~bpm,
	);
).quant_(~bpm);
