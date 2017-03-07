#!/usr/bin/env python

# gittools contains functions that deal with Git.

import os
import sys
import subprocess

BRANCH_NAME = "commit-art-dummy"	# name of git branch
REMOTE_NAME = "origin"			# name of git remote

def createGitDirectory(dirname):
	"""Creates and initializes a git directory at path: `dirname`.
	Will not overwrite an existing directory.
	"""
	# check if already exists, make dir name(s) provided by user
	if not os.path.exists(dirname):
		os.makedirs(dirname)
	else:
		sys.stderr.write("%s already exists.\n" % (dirname))
		return False
	try:
		origWD = os.getcwd()				# save cwd
		os.chdir(dirname)				# change to newly created dir
		subprocess.call(['git', 'init', '--quiet'])	# initialize git
		os.chdir(origWD)				# change back to original wd
		return True
	except Exception as e:
		sys.stderr.write("Unable to `git init` directory: %s\n%s\n" % (dirname, str(e)))
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

def gitCommit(date):
	"""Commits in CWD at given date."""
	subprocess.call(['git', 'commit', '--allow-empty', '--date=\'{}\''.format(date), '-m', 'update history', '--quiet'])

def pushToRemote(gitdirname, remoteURL):
	origWD = os.getcwd()
	os.chdir(gitdirname)
	subprocess.call(['git', 'remote', 'add', REMOTE_NAME, remoteURL])
	subprocess.call(['git', 'push', REMOTE_NAME, BRANCH_NAME, '--quiet'])
	os.chdir(origWD)

