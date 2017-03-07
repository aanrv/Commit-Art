#!/usr/bin/env python

import os
import sys
import subprocess
import functools

import ghgraph
import gittools

def getCoordinates(filename):
	"""Retrieves coordinates from a file created by the user."""
	coordinateList = []
	with open(filename, 'r') as f:
		for line in f:
			# get coordinate strings
			xy = line.split(',')

			# validate format
			if (len(xy) != 2):
				sys.stderr.write("Invalid format in line: %s.\n" % (line.rstrip('\n')))
				continue
			strx = xy[0]
			stry = xy[1].rstrip('\n')
			if (not isValidDigit(strx) or not isValidDigit(stry)):
				sys.stderr.write("Invalid format in line: %s.\n" % (line))
				continue
			
			# check date is in bounds
			(x,y) = (int(strx), int(stry))
			if (not ghgraph.validCoordinate((x,y))):
				sys.stderr.write("Coordinate %s is out of bounds.\n" % (line.rstrip('\n')))
				continue

			# all checks completed, append coordinates
			coordinateList.append((x,y))
	return coordinateList

def createCommits(clist, dirname):
	"""Creates commits at points in `clist` in Git directory `dirname`.
	Precondition: The points in clist are sorted by the dates they represent."""
	origWD = os.getcwd()				# save curr dir
	os.chdir(dirname)				# change to git dir
	for point in clist:
		pointdate = ghgraph.coordinateToDate(point)	# get date at point
		gitDate = gittools.createGitDate(pointdate)	# get date string in git format
		gittools.gitCommit(gitDate)			# create an empty commit at given date
	subprocess.call(['git', 'branch', '-m', gittools.BRANCH_NAME])
	os.chdir(origWD)

def isValidDigit(digitStr):
	try:
		int(digitStr)
		return True;
	except:
		return False;

def main():
	# make sure args are properly provided
	if (not (len(sys.argv) >= 3 and len(sys.argv) <= 4)):
		print("Usage: %s coordinatesFile newDirectoryName [remoteURL]" % (sys.argv[0]))
		sys.exit(1)

	# retrieve coordinates from file
	filename = sys.argv[1]
	print("Retrieving coordinates from file: %s" % (filename))
	clist = sorted(set(getCoordinates(sys.argv[1])), key=functools.cmp_to_key(ghgraph.cmpPoints))	# retrieve coordinates from file

	# create and init git directory
	gitdirname = sys.argv[2]
	print("Creating git directory at: %s" % gitdirname)
	if (not gittools.createGitDirectory(gitdirname)):
		sys.exit(1)

	# create commits based on coordinates
	print("Creating commits")
	createCommits(clist, gitdirname)

	# if extra arg provided, push directory to remote
	if (len(sys.argv) == 4):
		remote = sys.argv[3]
		print("Pushing to remote: %s" % remote)
		gittools.pushToRemote(gitdirname, remote)
	
	print("Done")

if __name__ == '__main__':
	main()

