#!/usr/bin/python

import sys
import datetime

DAYS_IN_WEEK = 7

# calculate the current origin's (0,0) date
def calc_origin():
	COLS = 54						# number of cols in commit history grid

	reference_origin = datetime.datetime(2016, 2, 28, 0, 0)	# a known past origin used as a reference to find current origin
	now = datetime.datetime.today()

	# perform super advanced quantum mathematical calculations
	delta_days = ((now - reference_origin).days % 7)
	origin = now - datetime.timedelta(days=delta_days) - datetime.timedelta(days=((COLS - 1) * DAYS_IN_WEEK))
	
	return origin

def coordinate_to_date(dweeks, ddays):
	origin = calc_origin()
	return origin + datetime.timedelta(days=(dweeks * DAYS_IN_WEEK)) + datetime.timedelta(days=ddays)

def get_coordinates(filename):
	coordinate_list = []
	with open(filename) as f:
		for line in f:
			x = line.split(',')[0]
			y = line.split(',')[1].rstrip('\n')
			if (not isValidDigit(x) or not isValidDigit(y)):	# make sure string is properly formatted
				print("Invalid format in line: " + line)
				continue
			coordinate_list.append( (int(x), int(y)) )
	return coordinate_list

def isValidDigit(digit_str):
	try:
		int(digit_str)
		return True;
	except:
		return False;

def main():
	clist = list(set(get_coordinates(sys.argv[1])))	# retrieve coordinates from file, remove dups using set
	print clist

if __name__ == '__main__':
  main()

