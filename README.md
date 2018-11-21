# shmidi
Shorthand MIDI in Python. 

# why?


# background
This project came from my personal desire to have a shorthand way to compose music. 

I figurd there was something out there already written that could do this, but I was pleasently surprised with what I discovered.

My original thought was to abstract up one level the concept of notes, so instead of saying what key you're in. This means you could describe a melody with just numbers 1 through 7, as long as you have a way to indicite if you are going up or down an octave.

I was happy to find there is alreay a system in place that is very similar to this, referred to as Chinese Musical Notation (Numbered System). It's amazingly simple, and with a few tweaks can be mapped to a Python-friendly format (ASCII).

For reference, you can view a nice write-up on this sytem by Stanford Chinese Music Ensemble at https://web.stanford.edu/group/scme/cgi-bin/wordpress1/chinese-music-%E4%B8%AD%E5%9B%BD%E9%9F%B3%E4%B9%90/chinese-musical-notation-numbered-system 

# use

<pre><code>>>> import shmidi
>>> rainbow = '1 - 1^ - | 7 5/ 6/ 7 1^ | 1 - 6 - | 5 - - -'
>>> song = shmidi.compile(rainbow, key='Eb') #TODO - implement key, saving to variable (song), MIDI file header/ meta, and note_off !
note_on channel=0 note=60 velocity=64 time=1920
note_on channel=0 note=72 velocity=64 time=1920
note_on channel=0 note=71 velocity=64 time=960
note_on channel=0 note=67 velocity=64 time=480
note_on channel=0 note=69 velocity=64 time=480
note_on channel=0 note=71 velocity=64 time=960
note_on channel=0 note=72 velocity=64 time=960
note_on channel=0 note=60 velocity=64 time=1920
note_on channel=0 note=69 velocity=64 time=1920
note_on channel=0 note=67 velocity=64 time=3840
</code>