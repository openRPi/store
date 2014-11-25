import pygame, sys
from pygame.locals import *

import datetime
import psutil
import socket
import fcntl
import struct

pygame.init()

FPS         = 1
LINE_HIGH   = 20
BG_COLOR    = (221, 72, 20)

label_color = (255,255,255)
text_color  = (255,255,255)

def get_cpu_str():
	return "%d%%" %(psutil.cpu_percent(),)

def get_mem_str():
	vm = psutil.virtual_memory()
	return '%d%% %s/%sM' %(vm.percent, vm.used/1024/1024, vm.total/1024/1024)

def get_swap_str():
	swap = psutil.swap_memory()
	return '%d%% %s/%sM' %(swap.percent, swap.used/1024/1024, swap.total/1024/1024)

def get_disk_str():
	disk = psutil.disk_usage('/')
	return '%d%% %s/%sM' %(disk.percent, disk.used/1024/1024, disk.total/1024/1024)

def get_ip_str(ifname='eth0'):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		return socket.inet_ntoa(
			fcntl.ioctl(
				s.fileno(),
					0x8915,  # SIOCGIFADDR
					struct.pack('256s', ifname[:15]))[20:24])
	except:
		return 'None'

def get_now_str(micro=False):
	s = "%Y-%m-%d %H:%M:%S"
	if micro:
		s += '.%f'
	return datetime.datetime.today().strftime(s)

display_disgn = (
	(dict(text='CPU', width=60, color=label_color),
		dict(text=get_cpu_str, width=80, color=text_color)),
	(dict(text='MEM', width=60, color=label_color),
		dict(text=get_mem_str, width=80, color=text_color)),
	(dict(text='SWAP', width=60, color=label_color),
		dict(text=get_swap_str, width=80, color=text_color)),
	(dict(text='DISK', width=60, color=label_color),
		dict(text=get_disk_str, width=80, color=text_color)),
	# IP
	(dict(text='IP', width=60, color=label_color),
		dict(text=lambda : 'eth0  %s' %(get_ip_str('eth0'),), width=80, color=text_color),),
	(dict(text='', width=60, color=label_color),
		dict(text=lambda : 'wlan0 %s' %(get_ip_str('wlan0'),), width=80, color=text_color)),
	# 
	(dict(text='Time', width=60, color=label_color),
		dict(text=get_now_str, width=80, color=text_color)))


fpsClock = pygame.time.Clock()
# set up the window
display_surf = pygame.display.set_mode((0, 0), pygame.FULLSCREEN|pygame.NOFRAME, 32)
pygame.display.set_caption('Test')
pygame.mouse.set_visible(False)

text_surf  = pygame.font.SysFont('courier new',LINE_HIGH)

while True:
	display_surf.fill(BG_COLOR)

	for i,line in enumerate(display_disgn):
		left_width = 0
		for item in line:
			text    = str(item['text']())  if callable(item['text'])  else item['text']
			width   = str(item['width']()) if callable(item['width']) else item['width']
			color   = str(item['color']()) if callable(item['color']) else item['color']
			display_surf.blit(text_surf.render(text,False,color),(left_width,i*LINE_HIGH))
			left_width += width

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	pygame.display.update()
	fpsClock.tick(FPS)
