import mido

mid = mido.MidiFile('midi_files/mary_had_a_little_lamb_pno.mid')

cumtime = 0
tempo = 0

for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        try:
            tempo = msg.tempo
        except:
            pass
        cumtime += msg.time
        print(msg, f'Cum_Time={round(mido.tick2second(cumtime, 960, tempo), 1)}') 