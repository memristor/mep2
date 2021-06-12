#!/usr/bin/env python3
# use as separate program used with sudo
import RPi.GPIO as GPIO
import time
import threading
GPIO.setmode(GPIO.BCM)

import socket
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 3500))
s.listen(1)
conn = False

GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(14, GPIO.OUT, initial=0)

def gen_func(pin):
	def fnc(channel):
		time.sleep(0.01)
		if conn:
			conn.send(b'05' + bytes([GPIO.input(5)+0x30]))
	return fnc

def b5(channel):
	time.sleep(0.01)
	if conn:
		conn.send(b'05' + bytes([GPIO.input(5)+0x30]))

def b15(channel):
	
	time.sleep(0.1)
	a = b'15' + bytes([GPIO.input(15)+0x30])
	print('rxd',a)
	if conn:
		conn.send(a)

def b6(channel):
	time.sleep(0.01)
	if conn:
		conn.send(b'06' + bytes([GPIO.input(6)+0x30]))

def b13(channel):
	if conn:
		conn.send(b'13' + bytes([GPIO.input(13)+0x30]))

def b19(channel):
	if conn:
		conn.send(b'19' + bytes([GPIO.input(19)+0x30]))

GPIO.add_event_detect(5, GPIO.BOTH, callback=b5, bouncetime=1000)
GPIO.add_event_detect(6, GPIO.BOTH, callback=b6, bouncetime=1000)
GPIO.add_event_detect(13, GPIO.FALLING, callback=b13, bouncetime=1000)
GPIO.add_event_detect(19, GPIO.FALLING, callback=b19, bouncetime=1000)

GPIO.add_event_detect(15, GPIO.BOTH, callback=b15, bouncetime=300)



#conn = None
#def polling(a):
#	old_c = -1
#	while 1:
#		time.sleep(0.1)
#		c = GPIO.input(5)
#		print('test ', c)
#		if c !=	old_c:
#			old_c = c
#			if conn:
#				conn.send(b'05' + bytes([c+0x30]))
#
#x=threading.Thread(target=polling, args=(1,))
#x.start()
while 1:
        conn, addr = s.accept()

GPIO.cleanup()
