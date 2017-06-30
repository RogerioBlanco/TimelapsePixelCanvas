#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sched, time, os, math, datetime

from argparse import ArgumentParser
from urllib2 import Request as request, urlopen
from PIL import Image

BLOCK_SIZE = 64
AREA_LEFT = 7
AREA_RIGHT = 8
TOTAL_AREA = AREA_LEFT + AREA_RIGHT
AREA_SIZE = TOTAL_AREA * BLOCK_SIZE
AREA = AREA_SIZE * AREA_SIZE

COLORS = [
	(255, 255, 255),
	(228, 228, 228),
	(136, 136, 136),
	(34, 34, 34),
	(255, 167, 209),
	(229, 0, 0),
	(229, 149, 0),
	(160, 106, 66),
	(229, 217, 0),
	(148, 224, 68),
	(2, 190, 1),
	(0, 211, 221),
	(0, 131, 199),
	(0, 0, 234),
	(207, 110, 228),
	(130, 0, 128)
]

URL = 'http://pixelcanvas.io/api/bigchunk/%s.%s.bmp'

def download_bmp(x, y):
	return urlopen(request(URL % (x, y), headers = {'User-agent':'timelapse bot'})).read()

def parse_args():
	parser = ArgumentParser()
	parser.add_argument('-s' ,'--seconds', required=False, type=int, default=30, dest='seconds')
	parser.add_argument('-r', '--radius', required=False, type=int , default=1, dest='radius')
	parser.add_argument('-x', required=False, type=int, dest='x')
	parser.add_argument('-y', required=False, type=int, dest='y')
	parser.add_argument('-d','--directory', required=False, default='./', dest='directory')
	parser.add_argument('--start_x', required=False, type=int, dest='start_x')
	parser.add_argument('--end_x', required=False, type=int, dest='end_x')
	parser.add_argument('--start_y', required=False, type=int, dest='start_y')
	parser.add_argument('--end_y', required=False, type=int, dest='end_y')
	#parser.add_argument('--proxy_url', required=False, dest='proxy_url', help='Proxy url with port. ex: url:port')
	#parser.add_argument('--proxy_auth', required=False, dest='proxy_auth', help='Proxy authentication. ex: user:pass')

	return parser.parse_args()

def valide_args(args):

	if all(v is None for v in [args.x, args.y]) and all(v is None for v in [args.start_x, args.end_x, args.start_y, args.end_y]):
		raise ValueError("It's necesary choose or the -x axis and -y axis or --start_y, --start_x, --end_y, --end_x arguments")

	if all(v is None for v in [args.x, args.y]) and None in [args.start_x, args.end_x, args.start_y, args.end_y]:
		raise ValueError("It's necessary fill all the parameters --start_y, --start_x, --end_y, --end_x")
	
	if None in [args.x, args.y] and all(v is None for v in [args.start_x, args.end_x, args.start_y, args.end_y]):
		raise ValueError("It's necessary fill all the parameters -x, -y")

	if all(not v is None for v in [args.x, args.y]) and all(not v is None for v in [args.start_x, args.end_x, args.start_y, args.end_y]):
		raise ValueError('You need pick or the -x axis and -y axis or --start_y, --start_x, --end_y, --end_x arguments')

	if args.seconds < 1:
		raise ValueError("The seconds must be positive and non-zero")

	if all(v is None for v in [args.x, args.y]):
		if args.radius < 1:
			raise ValueError("The radius must be positive and non-zero and odd")

		if not args.radius % 2:
			raise ValueError("The radius must be odd")

def calc_radius(arg_radius, start_x, end_x, start_y, end_y):
	if all(not v is None for v in [start_x, end_x, start_y, end_y]):
		radius_x = abs((end_x - start_x) / AREA_SIZE)
		radius_y = abs((end_y - start_y) / AREA_SIZE)
		radius = int(math.ceil(radius_x if radius_x >= radius_y else radius_y))
		return (radius if radius % 2 else radius + 1)
	return arg_radius

def calc_size_area(radius):
	return (radius^2) * AREA

def get_points(x, y, start_x, end_x, start_y, end_y):
	if all(not v is None for v in [x, y]):
		return x, y

	return (end_x + start_x) / 2, (end_y + start_y) / 2

def setup_map_image(iteration, point_x, point_y):
	map_image = {}
	last = 0
	for x in xrange((point_x - (iteration + AREA_LEFT)) * BLOCK_SIZE, (iteration + AREA_RIGHT + point_x) * BLOCK_SIZE):
		map_image[x] = {}
		for y in xrange((point_y - (iteration + AREA_LEFT)) * BLOCK_SIZE, (iteration + AREA_RIGHT + point_y) * BLOCK_SIZE):
			map_image[x][y] = None
	return map_image

def get_iteration(radius):
	return int(math.ceil(radius / 2) * TOTAL_AREA)

def bigchunck(radius, point_x, point_y):
	point_x, point_y = (point_x - (point_x % BLOCK_SIZE)) / BLOCK_SIZE, (point_y - (point_y % BLOCK_SIZE)) / BLOCK_SIZE
	iteration = get_iteration(radius)
	map_image = setup_map_image(iteration, point_x, point_y)

	for center_x in xrange(point_x - iteration, 1 + point_x + iteration, TOTAL_AREA):
		for center_y in xrange(point_y - iteration, 1 + point_y + iteration, TOTAL_AREA):
			raw = download_bmp(center_x, center_y)
			index = 0
			for block_y in xrange(center_y - AREA_LEFT, center_y + AREA_RIGHT):
				for block_x in xrange(center_x - AREA_LEFT, center_x + AREA_RIGHT):
					for y in xrange(BLOCK_SIZE):
						actual_y = block_y * BLOCK_SIZE + y
						for x in xrange(0, BLOCK_SIZE, 2):
							actual_x = block_x * BLOCK_SIZE + x
							map_image[actual_x    ][actual_y] = ord(raw[index]) >> 4
							map_image[actual_x + 1][actual_y] = ord(raw[index]) & 0x0F
							index += 1
	return map_image

def get_sizes(radius, x, y, start_x, end_x, start_y, end_y):
	if all(not v is None for v in [start_x, end_x, start_y, end_y]):
		return abs(end_x - start_x), abs(end_y - start_y)
	return abs(calc_size_area(radius)), abs(calc_size_area(radius))

def create_image(width, height):
	image = Image.new('RGB', (width, height), (255,255,255))
	pix = image.load()
	return image, pix

def convert_custom_image(map_image, pix, start_x, end_x, start_y, end_y):	
	minor_x = (start_x if start_x < end_x else end_x)
	bigger_x = (start_x if start_x > end_x else end_x)

	minor_y = (start_y if start_y < end_y else end_y)
	bigger_y = (start_y if start_y > end_y else end_y)
	
	pix_x, pix_y = 0, 0
	
	for x in xrange(minor_x, bigger_x - 1 ):
		pix_y = 0
		for y in xrange(minor_y, bigger_y - 1):
			pix[pix_x, pix_y] = COLORS[map_image[x][y]]
			pix_y += 1
		pix_x += 1

	return pix

def convert_image_total(map_image, pix, radius, point_x, point_y):
	iteration = get_iteration(radius)
	#for x in xrange((point_x - (iteration + AREA_LEFT)) * BLOCK_SIZE, (iteration + AREA_RIGHT + point_x) * BLOCK_SIZE):
	#	for y in xrange((point_y - (iteration + AREA_LEFT)) * BLOCK_SIZE, (iteration + AREA_RIGHT + point_y) * BLOCK_SIZE):
	#		for block_y in xrange(center_y - AREA_LEFT, center_y + AREA_RIGHT):
	#			for block_x in xrange(center_x - AREA_LEFT, center_x + AREA_RIGHT):
	#		pix[pix_x, pix_y] = COLORS[map_image[x][y]]
	#		pix_y += 1
	#	pix_x += 1
	return pix

def save_image(image, directory):
	if not os.path.exists(directory):
		os.makedirs(directory)
	name_file = os.path.join(directory, datetime.datetime.utcnow().strftime("%Y%m%d%H%MUTC") + '.png')
	image.save(name_file)
	pass

def main():
	args = parse_args()

	valide_args(args)

	point_x, point_y = get_points(args.x, args.y, args.start_x, args.end_x, args.start_y, args.end_y)

	radius = calc_radius(args.radius, args.start_x, args.end_x, args.start_y, args.end_y)

	width, height = get_sizes(radius, args.x, args.y, args.start_x, args.end_x, args.start_y, args.end_y)	
	
	map_image = bigchunck(radius, point_x, point_y)

	image, pix = create_image(width, height)

	if all(not v is None for v in [args.start_x, args.end_x, args.start_y, args.end_y]):
		image.pix = convert_custom_image(map_image, pix, args.start_x, args.end_x, args.start_y, args.end_y)
	else:
		image.pix = convert_image_total(map_image, pix, radius, point_x, point_y)

	save_image(image, args.directory)

if __name__ == '__main__':	
	try:
		main()
	except KeyboardInterrupt:
		print 'Bye'