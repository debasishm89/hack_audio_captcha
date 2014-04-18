'''

Generate separate wav files depending on the loud voice detected in audio captcha challenge.
Author : Debasish Mandal
http://www.debasish.in/

'''

import wave
import sys
import struct
import os
import time
import httplib
from random import randint

ip = wave.open(sys.argv[1], 'r')
info = ip.getparams()
frame_list = []
for i in range(ip.getnframes()):
	iframe = ip.readframes(1)
	amplitude = struct.unpack('<h', iframe)[0]
	frame_list.append(amplitude)
ip.close()
for i in range(0,len(frame_list)):
	if abs(frame_list[i]) < 25:
		frame_list[i] = 0
################################  Find Out most noisy portions of the audio file ###########################
thresh = 30
output = []
non_zero_temp = []
length = len(frame_list)
i = 0
while i < length:
    zeros = []
    while i < length and frame_list[i] == 0:
        i += 1
        zeros.append(0)
    if len(zeros) != 0 and len(zeros) < thresh:
        non_zero_temp += zeros
    elif len(zeros) > thresh:
        if len(non_zero_temp) > 0 and i < length:
            output.append(non_zero_temp)
            non_zero_temp = []
    else:
        non_zero_temp.append(frame_list[i])
        i += 1
if len(non_zero_temp) > 0:
    output.append(non_zero_temp)

chunks = []
for j in range(0,len(output)):
	if len(output[j]) > 3000:
		chunks.append(output[j])
#########################################################################################################

for l in chunks:
	for m in range(0,len(l)):
		if l[m] == 0:
			 l[m] = randint(-0,+0)

inc_percent = 1	#10 percent

for l in chunks:
	for m in range(0,len(l)):
		if l[m] <= 0:
			# negative value
			l[m] = 0 - abs(l[m]) + abs(l[m])*inc_percent/100
		else:
			#positive vaule
			l[m] =     abs(l[m]) + abs(l[m])*inc_percent/100

########################################################

#Change it to > 1 if any amplification is required
NEW_RATE = 1

print '[+] Possibly ',len(chunks),'number of loud voice detected...'
for i in range(0, len(chunks)):
	new_frame_rate = info[0]*NEW_RATE
	print '[+] Creating No. ',str(i),'file..'
	split = wave.open('cut_'+str(i)+'.wav', 'w')

	split.setparams((info[0],info[1],info[2],0,info[4],info[5]))
#	split.setparams((info[0],info[1],new_frame_rate,0,info[4],info[5]))

	#Add some silence at start selecting +15 to -15
	for k in range(0,10000):
		single_frame = struct.pack('<h', randint(-25,+25))
		split.writeframes(single_frame)
	# Add the voice for the first time
	for frames in chunks[i]:
		single_frame = struct.pack('<h', frames)
		split.writeframes(single_frame)

	#Add some silence in between
	for k in range(0,10000):
		single_frame = struct.pack('<h', randint(-25,+25))
		split.writeframes(single_frame)

	# Add the voice second time
	for frames in chunks[i]:
		single_frame = struct.pack('<h', frames)
		split.writeframes(single_frame)

	#Add silence at end
	for k in range(0,10000):
		single_frame = struct.pack('<h', randint(-25,+25))
		split.writeframes(single_frame)

	split.close()
	time.sleep(1)
	print '[+] Done!'
