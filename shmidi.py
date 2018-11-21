import time

import mido
from mido import Message

import midisly

msgs = [Message('note_on', note=n) for n in range(30, 100, 2)]

# outport = mido.open_output('virtual', virtual=True)

# for msg in msgs:
#     outport.send(msg)
#     time.sleep(.03)

class Note:
    def __init__(self, note_number=1, channel=0, velocity=64, time=0, length=960, root='C'): # length of 960 is standard quarter note
        self.note_number = note_number
        self.channel = channel
        self.note = self.convert_number_to_midi(self.note_number)
        self.velocity = velocity
        self.time = time
        self.length = length
    
    @staticmethod
    def convert_number_to_midi(num):
        num = str(num)
        temp_dict = {
            '1': 60,
            '2': 62,
            '3': 64,
            '4': 65,
            '5': 67,
            '6': 69,
            '7': 71,
            '8': 72,
            '2+': 74,
            '3+': 76
        }
        
        return temp_dict.get(num)
    
    def return_msg(self):
        return Message('note_on', note=self.note, velocity=self.velocity, time=self.length)


class Melody:
    def __init__(self, notes, outport=None, sleep=.2):
        self.notes = notes
        self.outport = outport
        self.sleep = sleep
        self.melody = self._create_melody() if self.notes else []
    
    def __str__(self):
        return '\n'.join([str(note) for note in self.melody])
    
    def _create_melody(self):
        return [Note(num).return_msg() for num in self.notes]
        
    def play(self):
        for msg in self.melody:
            self.outport.send(msg)
            time.sleep(self.sleep)

    def add_note(self, note):
        self.notes.append(note)
        self.melody = self._create_melody()

def compile(notes, **kwargs):
    lexer = midisly.ShmidiLexer()
    parser = midisly.ShmidiParser()
    parser.parse(lexer.tokenize(notes))

if __name__ == '__main__':

    melody = '''
            6v. 6v/ 6v 3 | 3 2 1 - | 7v. 7v/ 7v 1/ 7v/ | 6v - - - |
            6v/ 6v 6v/ 6 6/ 5/ | 6 5 3 - | 2/ 2 1/ 2 5 | 3 - - - |
            4/ 4 3/ 4/ 4 3/ | 4 3/ 2/ 1 - | '''
    
    mary = '3212333'

    twinkle = '1 1 5 5 6 6 5- 4 4 3 3 2 2 1- 5 5 4 4 3 3 2- 5 5 4 4 3 3 2- 1 1 5 5 6 6 5- 4 4 3 3 2 2 1-'

    print('melody')
    compile(melody)
    print('')
    print('mary')
    compile(mary)
    print()
    print('twinkle')
    compile(twinkle)