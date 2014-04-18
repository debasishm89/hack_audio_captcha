'''

Description : WAV file speed changes
Author : Debasish Mandal

'''
import wave
import sys

CHANNELS = 1
swidth = 2
Change_RATE = 1.3	# Default vaulue is 1

spf = wave.open(sys.argv[1], 'rb')
RATE=spf.getframerate()
signal = spf.readframes(-1)

wf = wave.open('output.wav', 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(swidth)
wf.setframerate(RATE*Change_RATE)
wf.writeframes(signal)
wf.close()
