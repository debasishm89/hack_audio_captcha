'''

Dumb noise remover.
Author: Debasish Mandal.

'''

import wave
import sys
import struct
ip = wave.open(sys.argv[1], 'r')
op = wave.open(sys.argv[2], 'w')
op.setparams(ip.getparams())

for i in range(ip.getnframes()):
	iframe = ip.readframes(1)
	amplitude = abs(struct.unpack('<h', iframe)[0])
	if amplitude < 3000:
		final_frame = '\x00\x00'
	else:
		final_frame = iframe
	op.writeframes(final_frame)
op.close()
ip.close()

