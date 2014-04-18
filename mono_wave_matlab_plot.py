import wave
import struct
import matplotlib.pyplot as plt

data_set = []
f = wave.open('fixed.wav', 'r')
print '[+] WAV parameters ',f.getparams()
print '[+] No. of Frames ',f.getnframes()
for i in range(f.getnframes()):
	single_frame = f.readframes(1)
	sint = struct.unpack('<h', single_frame)[0]
	data_set.append(sint)
f.close()
plt.plot(data_set)
plt.ylabel('Amplitude')
plt.xlabel('Time')
plt.show()
