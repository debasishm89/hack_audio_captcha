'''
Description : Noise removal script using FFT and IFT
Author : Debasish Mandal
Blog :  http://www.debasish.in/

'''

import wave
import sys
import struct
import numpy as np

ip = wave.open(sys.argv[1], 'r')

op = wave.open(sys.argv[2], 'w')
op.setparams(ip.getparams())

raw_frames = ip.readframes(ip.getnframes())
signal = np.fromstring(raw_frames, 'Int16')

mono = np.fft.rfft(signal)

lowpass = 21
highpass = 9000
mono[:lowpass] = 0
mono[500000:520000] = 0
mono[:highpass] = 0
ift_result = np.fft.irfft(mono)
no_noise = ift_result.astype(np.int16)
op.writeframes(no_noise.tostring())
op.close()
ip.close()

