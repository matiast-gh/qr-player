import zbarlight
import os
import sys
import PIL
import time

current_qr = ''

while True:

	try:
		f = 1
		qr_count = len(os.listdir('qr_codes'))
		os.system('sudo fswebcam -d /dev/video'+sys.argv[1]+' -q qr_codes/qr_'+str(qr_count)+'.jpg')
	except:
		f = 0
		if (current_qr != ''):
			os.system('sudo killall -9 omxplayer.bin > /dev/null 2>&1')
			current_qr = ''

	if (f):
		f = open('qr_codes/qr_'+str(qr_count)+'.jpg','rb')
		qr = PIL.Image.open(f);
		qr.load()

		codes = zbarlight.scan_codes('qrcode',qr)
		if (codes==None):
			os.remove('qr_codes/qr_'+str(qr_count)+'.jpg')

			if (current_qr != ''):
				os.system('sudo killall -9 omxplayer.bin > /dev/null 2>&1')
				current_qr = ''
		else:
			os.remove('qr_codes/qr_'+str(qr_count)+'.jpg')

			print 'QR: '+codes[0]

			if (current_qr != codes[0]):
				current_qr = codes[0]
				if (codes[0] != ''):
					if (os.path.isfile('music/'+codes[0]+'.mp3')):
						os.system('sudo killall -9 omxplayer.bin > /dev/null 2>&1')
						os.system('omxplayer -o local music/'+codes[0]+'.mp3 &')

	time.sleep(2)
