#!/usr/bin/env python

import sys
import os
import datetime
import subprocess
import functools

NUM_COLS = 53				# number of columns in GitHub's commit grid
DAYS_IN_WEEK = 7			# self-explanatory; you should not even be reading this comment
BRANCH_NAME = "commit-art-dummy"	# name of git branch
REMOTE_NAME = "origin"			# name of git remote

def calcOrigin(now):
	"""Calculates the date of the origin point (0,0) on GitHub's commit grid relative to `now`."""
	daysAfterSunday = (now.weekday() + 1) % DAYS_IN_WEEK		# calculate days after sunday (GitHub's graph has Sundays at y=0)
	deltaDays = daysAfterSunday + ((NUM_COLS - 1) * DAYS_IN_WEEK)	# calculates number of weeks (x)
	origin = now - datetime.timedelta(days=deltaDays)
	return origin

def coordinateToDate(xy):
	"""Converts a coordinate tuple to a date."""
	dweeks = xy[0]
	ddays = xy[1]
	origin = calcOrigin(datetime.datetime.now())
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
		return False
	try:
		origWD = os.getcwd()			# save cwd
		os.chdir(dirname)			# change to newly created dir
		subprocess.call(["git", "init"])	# initialize git
		os.chdir(origWD)			# change back to original wd
		return True
	except Exception as e:
		print("Unable to `git init` directory: %s\n%s" % (dirname, str(e)))
		return False

def createGitDate(date):
	"""Creates a date string in a format accepted by Git"""
	days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
	months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

	dayname = days[date.weekday()]
	day = str(date.day)
	month = months[date.month - 1]
	time = str(date.time()).split('.')[0]
	year = str(date.year)
	
	gitdate = "{} {} {} {} {}".format(dayname, month, day, time, year)
	return gitdate

def createCommits(clist, dirname):
	""" Creates commits at points in `clist` in Git directory `dirname`.
	Precondition: The points in clist are sorted by the dates they represent."""
	origWD = os.getcwd()				# save curr dir
	os.chdir(dirname)				# change to git dir
	for point in clist:
		pointdate = coordinateToDate(point)	# get date at point
		gitDate = createGitDate(pointdate)	# get date string in git format
		gitCommit(gitDate)				# create an empty commit at given date
	print("")
	subprocess.call(['git', 'branch', '-m', BRANCH_NAME])	# slight preemption against user accidentially pushing to wrong repo, master will not be affected
	print("")
	os.chdir(origWD)

def gitCommit(date):
	"""Commits in CWD at given date."""
	subprocess.call(['git', 'commit', '--allow-empty', '--date=\'{}\''.format(date), '-m', 'update history'])

def cmpPoints(p1, p2):
	"""A compare function to compare points without having to convert to datetime objects.
	Uses less space and performs fewer calculations."""
	p1x = p1[0]
	p1y = p1[1]
	p2x = p2[0]
	p2y = p2[1]
	return (p1x * 7 + p1y) - (p2x * 7 + p2y)

def pushToRemote(gitdirname, remoteURL):
	origWD = os.getcwd()
	os.chdir(gitdirname)

	subprocess.call(['git', 'remote', 'add', REMOTE_NAME, remoteURL])
	subprocess.call(['git', 'remote', '-v'])
	print("")
	subprocess.call(['git', 'push', REMOTE_NAME, BRANCH_NAME])
	
	os.chdir(origWD)

def main():
	# make sure args are provided
	if (not (len(sys.argv) >= 3 and len(sys.argv) <= 4)):
		print("Usage: %s coordinatesFile newDirectoryName [remoteURL]" % (sys.argv[0]))
		sys.exit(1)

	# retrieve coordinates from file
	filename = sys.argv[1]
	print("Retrieving coordinates from file: %s" % (filename))
	clist = sorted(set(getCoordinates(sys.argv[1])), key=functools.cmp_to_key(cmpPoints))	# retrieve coordinates from file
	print("\nRetrieved:")
	print(clist)
	print("")

	# create and init git directory
	gitdirname = sys.argv[2]
	if (not createGitDirectory(gitdirname)):
		sys.exit(1)

	# create commits
	createCommits(clist, gitdirname)

	# if extra arg provided, push directory to remote
	if (len(sys.argv) == 4):
		remote = sys.argv[3]
		pushToRemote(gitdirname, remote)
	
if __name__ == '__main__':
	main()

