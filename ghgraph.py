#!/usr/bin/env python

# ghgraph contains functions and variables that have to do with GitHub's commit graph.

import datetime

NUM_COLS = 53				# number of columns in GitHub's commit grid
DAYS_IN_WEEK = 7			# self-explanatory; you should not even be reading this comment

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

def validCoordinate(xy):
	x = xy[0]
	y = xy[1]
	return (x >= 0 and y >= 0 and x < NUM_COLS and y < DAYS_IN_WEEK)

def cmpPoints(p1, p2):
	"""A compare function to compare points without having to convert to datetime objects.
	Uses less space and performs fewer calculations."""
	p1x = p1[0]
	p1y = p1[1]
	p2x = p2[0]
	p2y = p2[1]
	return (p1x * DAYS_IN_WEEK + p1y) - (p2x * DAYS_IN_WEEK + p2y)

