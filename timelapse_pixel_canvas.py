#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sched, time, os, math
from argparse import ArgumentParser
from urllib2 import Request as request, urlopen

BLOCK_LENGTH = 64
AREA_LEFT = -7
AREA_RIGHT = 8
TOTAL_AREA = (abs(AREA_LEFT) + AREA_RIGHT)
AREA_LENGHT = TOTAL_AREA * BLOCK_LENGTH
AREA = AREA_LENGHT * AREA_LENGHT

URL = 'http://pixelcanvas.io/api/bigchunk/%s.%s.bmp'

def download_bmp(x, y):
	return urlopen(request(URL % (x, y), headers = {'User-agent':'timelapse bot'})).read()

def parse_args():
	parser = ArgumentParser()
	parser.add_argument('-s' ,'--seconds', required=False, type=int, default=30, dest='seconds')
	parser.add_argument('-r', '--radius', required=False, type=int , default=1, dest='radius')
	parser.add_argument('-x', required=False, type=int, dest='x')
	parser.add_argument('-y', required=False, type=int, dest='y')
	parser.add_argument('-d','--directory', required=False, dest='directory')
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
		radius_x = abs((end_x - start_x) / AREA_LENGHT)
		radius_y = abs((end_y - start_y) / AREA_LENGHT)
		radius = int(math.ceil(radius_x if radius_x >= radius_y else radius_y))
		return (radius if radius % 2 else radius + 1)
	return arg_radius

def calc_area(radius):
	return (radius^2) * AREA

def get_points(x, y, start_x, end_x, start_y, end_y):
	if all(not v is None for v in [x, y]):
		return x, y

	return end_x - start_x, end_y - start_y

def bigchunck(radius, point_x, point_y):
	point_x, point_y = (point_x - (point_x % BLOCK_LENGTH)) / BLOCK_LENGTH, (point_x - (point_x % BLOCK_LENGTH)) / BLOCK_LENGTH

def main():
	args = parse_args()

	valide_args(args)

	point_x, point_y = get_points(args.x, args.y, args.start_x, args.end_x, args.start_y, args.end_y)

	radius = calc_radius(args.radius, args.start_x, args.end_x, args.start_y, args.end_y)
	
	map_image = bigchunck(radius, point_x, point_y)
	#print len(download_bmp(args.x, args.y))

if __name__ == '__main__':	
	main()