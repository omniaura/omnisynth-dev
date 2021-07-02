~bpm = (60/120)*4;
a = Scale.melodicMinor;

Pdef (
	\pattern3,
	Pbind(
		\instrument, \tone6,
		\scale, a,
		\degree, Pseq((0..2) ++ (7..5), inf), 
		\out, 0,
		\root, 15,
		\amp, Pexprand(0.1, 0.12, inf),
		\gate, 1,
		\mod_freq, Pexprand(1,100,inf),
		\mod_amp, 200,
		\lpf_cutoff, 10000, 
		\hpf_cutoff, 200,
		\attack_time, Pexprand(0.10, 0.20, inf), 
		\decay_time, 0.3, 
		\sustain, 0.4,
		\release_time, 0.2,
		\lin_start, 100, 
		\lin_stop, 1,
		\lin_duration, 0.05,
		\bias, 0.0,
		\dur, Prand([
			Pseq([1/16], 32),
			Pseq([1/4],8),
			Pseq([1/12],12)
			], inf),
		\stretch, ~bpm,
	);
).quant_(~bpm);
