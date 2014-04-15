import re

def isValidIP(ip):
	"""Returns None if invalid, match object on IPv4 addr"""
	#the magic begins here
	p = re.compile('^(([1-9]?\d|1\d\d|25[0-5]|2[0-4]\d)\.){3}([1-9]?\d|1\d\d|25[0-5]|2[0-4]\d)$')
	return p.match(ip)

def isValidPort(port):
	"""Returns None if invalid, match object on Port Number"""
	pass