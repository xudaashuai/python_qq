import re
import threading
import time


def start_window_anim(weight, attr, duration, **kwargs):
	ss = re.split("[x+]", weight.winfo_geometry())
	index = 0
	if attr == 'height':
		index = 1
	elif attr == 'x':
		index = 2
	elif attr == 'y':
		index = 3
	ss[index] = '{0}'
	if 'start' not in kwargs:
		kwargs['start'] = int(weight.tk.getint(
			weight.tk.call('winfo', attr, weight._w)))
		kwargs['end'] = kwargs['start'] + kwargs['offset']
	threading.Thread(target=_anim_window, args=(weight, kwargs['start'],
	                                            kwargs['end'], duration,
	                                            "{0}x{1}+{2}+{3}".format(ss[0], ss[1], ss[2], ss[3]))).start()





def start_weight_anim(weight, attr, duration, **kwargs):
	if 'start' not in kwargs:
		kwargs['start'] = int(weight.place_info()[attr])
		kwargs['end'] = kwargs['start'] + kwargs['offset']
	threading.Thread(target=_anim_weight, args=(weight, kwargs['start'], kwargs['end'], duration, attr)).start()


def _anim_weight(weight, start, end, duration, attr):
	k = (end - start) / (duration / 15)
	for i in range(int(duration / 15)):
		start += k
		weight.place({attr: start})
		time.sleep(0.01)
	start = end
	weight.place({attr: start})


def _anim_window(weight, start, end, duration, attr):
	k = (end - start) / (duration / 15)
	for i in range(int(duration / 15)):
		start += k
		weight.geometry(attr.format(int(start)))
		time.sleep(0.01)
	start = end
	weight.geometry(attr.format(end))


def _anim_window_two(weight, startx, endx, starty, endy, duration, attr):
	kx = (endx - startx) / (duration / 15)
	ky = (endy - starty) / (duration / 15)
	for i in range(int(duration / 15)):
		startx += kx
		starty += ky
		weight.geometry(attr.format(int(startx), int(starty)))
		time.sleep(0.002)
	startx = endx
	starty = endy
	weight.geometry(attr.format(endx, endy))


def shake_window(weight, offset=10, times=5):
	threading.Thread(target=_shake_window, args=(weight, offset, times)).start()


def _shake_window(weight, offset, times):
	ss = re.split("[x+]", weight.winfo_geometry())
	startx = int(weight.tk.getint(
		weight.tk.call('winfo', 'x', weight._w)))
	endx = offset + startx
	starty = int(weight.tk.getint(
		weight.tk.call('winfo', 'y', weight._w)))
	endy = -offset + starty
	for i in range(times):
		_anim_window_two(weight, startx, endx, starty, endy, 100, "{0}x{1}+{2}+{3}".format(ss[0], ss[1], '{0}', '{1}'))
		_anim_window_two(weight, endx, startx, endy, starty, 100, "{0}x{1}+{2}+{3}".format(ss[0], ss[1], '{0}', '{1}'))
