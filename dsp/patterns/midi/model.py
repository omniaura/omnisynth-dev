import os


def pre_process(folder):
    corpus = []
    for file in os.listdir(folder):
        mid = MidiFile(folder + file)
        for msg in mid:
            if msg.is_meta:
                continue
            corpus.append(msg)

    raw_corpus = []
    for msg in corpus:
        if isinstance(msg, list): continue
        time = msg.time
        raw = msg.bytes()
        raw.append(time)
        raw_corpus.append(raw)
    return raw_corpus

def read_midi():
    with open('gen_midi.txt', 'r') as f:
        midi_string = f.read()
    print(midi_string)

if __name__=='__main__':
    folder = "lofi/"
    corpus = pre_process(folder)
    with open('corpus.txt', 'w') as f:
        for msg in corpus:
            f.write(str(msg)+"\n")
    # read_midi()