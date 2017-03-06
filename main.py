#!/usr/bin/python

import sys
import os
import datetime
import subprocess

NUM_COLS = 53		# number of columns in GitHub's commit grid
DAYS_IN_WEEK = 7	# self-explanatory; you should not even be reading this comment

def calcOrigin():
	"""Calculates the date of the origin point (0,0) on GitHub's commit grid relative to today's date."""
	referenceOrigin = datetime.datetime(2016, 2, 28, 0, 0)	# a known past origin used as a reference to find current origin
	now = datetime.datetime.today()
	
	# perform super advanced quantum mathematical calculations
	deltaDays = ((now - referenceOrigin).days % 7) + ((NUM_COLS - 1) * DAYS_IN_WEEK)
	origin = now - datetime.timedelta(days=deltaDays)
	return origin

def coordinateToDate(xy):
	"""Converts a coordinate tuple to a date."""
	dweeks = xy[0]
	ddays = xy[1]
	origin = calcOrigin()
	return origin + datetime.timedelta(days=(dweeks * DAYS_IN_WEEK)) + datetime.timedelta(days=ddays)

def getCoordinates(filename):
	"""Retrieves coordinates from a file created by the user."""
	coordinateList = []
	with open(filename, 'r') as f:
		for line in f:
			# get coordinate strings
			xy = line.split(',')

			# validate format
			if (len(xy) != 2):
				print("Invalid format in line: %s" % (line.rstrip('\n')))
				continue
			strx = xy[0]
			stry = xy[1].rstrip('\n')
			if (not isValidDigit(strx) or not isValidDigit(stry)):
				print("Invalid format in line: %s" % (line))
				continue
			
			# check date is in bounds
			x = int(strx)
			y = int(stry)
			if (x < 0 or y < 0 or x >= NUM_COLS or y >= DAYS_IN_WEEK):
				print("Coordinate %s is out of bounds." % (line.rstrip('\n')))
				continue

			# all checks completed, append coordinates
			coordinateList.append( (x,y) )
	return coordinateList

def isValidDigit(digitStr):
	try:
		int(digitStr)
		return True;
	except:
		return False;

def createGitDirectory(dirname):
	"""Creates and initializes a git directory at path: `dirname`.
	Will not overwrite an existing directory.
	"""
	# check if already exists, make dir name(s) provided by user
	if not os.path.exists(dirname):
		os.makedirs(dirname)
	else:
		print("%s already exists." % (dirname))
		return None
	try:
		origWD = os.getcwd()			# save cwd
		os.chdir(dirname)			# change to newly created dir
		subprocess.call(["git", "init"])	# initialize git
		os.chdir(origWD)			# change back to original wd
	except Exception as e:
		print("Unable to `git init` directory: %s\n%s" % (dirname, str(e)))
		return None

def main():
	# make sure args are provided
	if (len(sys.argv) != 3):
		print("Usage: %s coordinatesFile newDirectoryName" % (sys.argv[0]))
		sys.exit(1)

	# retrieve coordinates from file
	print("Retrieving coordinates from file: %s" % (sys.argv[1]))
	clist = list(set(getCoordinates(sys.argv[1])))	# retrieve coordinates from file
	print("\nRetrieved:")
	print(clist)
	print("")

	# create and init git directory
	if not createGitDirectory(sys.argv[2]):
		sys.exit(1)
	
if __name__ == '__main__':
	main()

