import httplib
import re
import time
import os

headers = {'Accept':'*/*','Accept-Encoding':'gzip,deflate,sdch','Accept-Language':'en-US,en;q=0.8','Connection':'keep-alive','Referer':'http://www.google.com/recaptcha/demo/'}


class Recaptcha:
	def downloadmp3(self):
		print '[+] Loading Capctha..'
		print '[+] Getting Captcha ID..'
		con = httplib.HTTPConnection('www.google.com')
		con.request("GET", "/recaptcha/demo/","",headers)
		match = re.findall('http://www.google.com(.*?)"></script>',con.getresponse().read())
		con.request("GET", match[0],'',headers)
		k = match[0][27:]
		print '[+] Captcha ID is..',k
		match = re.findall("challenge :(.*?)',",con.getresponse().read())
		challenge =  match[0]
		reload = '/recaptcha/api/reload?c='+ challenge[2:] +'&k='+ k +'&reason=a&type=audio&lang=en-GB&new_audio_default=1'
		print '[+] Reloading Captcha...'
		con.request("GET",reload,"",headers)
		print '[+] Getting Audio Challenge code...'
		match = re.findall("Recaptcha.finish_reload(.*?)audio",con.getresponse().read())
		print '[+] Downloading Audio..'
		con.request('GET', '/recaptcha/api/audio.mp3?c='+match[0][2:-4],'',headers)
		f = open('downloaded.mp3','wb')
		f.write(con.getresponse().read())
		f.close()
		print '[+] MP3 Saved!!'
		con.close()
if __name__ == "__main__":
	rcap = Recaptcha()
	rcap.downloadmp3()
