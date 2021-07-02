~bpm = (60/120)*4;
a = Scale.melodicMinor;

Pdef (
	\pattern2,
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

Pdef (
	\pattern2a,
	Pbind(
		\instrument, \tone8,
		\scale, a,
		\bend, ~bend.linlin(0,16383,-2,2),
		\degree, Pseq((9..8)++(6..7),inf),
		\root,Prand([10,15,17,20], inf),
		\out, 0,
		\amp, Pexprand(0.04, 0.05, inf),
		\gate, 1,
		\mod_freq, Pwhite(1000, 10000, inf),
		\lpf_cutoff, 20000, 
		\hpf_cutoff, 20,
		\attack_time, Pexprand(1.6, 2.8, inf), 
		\decay_time, 0.3, 
		\sustain, 0.4,
		\release_time, 3.2,
		\lin_start, 10, 
		\lin_stop, 2,
		\lin_duration, 0.05,
		\bias, 0.0,
		\legato, 4.0,
		\dur, Pseq([1,1,Rest(1)], inf),
		\stretch, ~bpm,
	);
).quant_(~bpm);

Pdef (
	\pattern2b,
	Pbind(
		\instrument, \tone8,
		\scale, a,
		\bend, ~bend.linlin(0,16383,-2,2),
		\degree, Pseq((4..3)++(0..1) ,inf),
		\root,3,
		\out, 0,
		\amp, Pexprand(0.04, 0.05, inf),
		\gate, 1,
		\mod_freq, Pwhite(1000, 10000, inf),
		\lpf_cutoff, 20000, 
		\hpf_cutoff, 20,
		\attack_time, Pexprand(1.6, 2.8, inf), 
		\decay_time, 0.3, 
		\sustain, 0.4,
		\release_time, 3.2,
		\lin_start, 10, 
		\lin_stop, 2,
		\lin_duration, 0.05,
		\bias, 0.0,
		\legato, 4.0,
		\dur, Pseq([1,1,Rest(1)], inf),
		\stretch, ~bpm,
	);
).quant_(~bpm);

Pdef (
	\pattern2c,
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