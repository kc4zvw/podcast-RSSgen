#!/usr/bin/python
#
# Author: David Billsbrough <billsbrough@gmail.com>
# Created: Sunday, July 05, 2015 at 08:23:20 AM (EDT)
# License: Generic Open Source License
# Warranty: None
# Version: $Revision: 0.4 $
#
# Purpose: generate a RSS file for a list of audio podcasts
#
# $Id: fetch-podcast-data.py,v 0.4 2015/07/05 11:08:56 kc4zvw Exp kc4zvw $

import os, shlex, string, subprocess, sys, time

def get_home_dir():
	myHOME = os.environ["HOME"]
	#print("My $HOME directory is %s.\n" % myHOME)
	return myHOME

def formattedDate(d):
	return time.strftime("%A, %B %d, %Y at %r", time.localtime(d))

def display_line(array):
	(Item, Title, PubDate, Links, Author, Comments, Category, AudioURL, Length, Desc) = array
	print "  The title is %s and the URL is %s." % (Title, AudioURL)

def process_line(aline):
	aline.strip
	#print("Line: %s" % aline)
	(Item, Title, PubDate, Links, Author, Comments, Category, AudioURL, Length, Desc) = aline.split("|")
	all_fields = (Item, Title, PubDate, Links, Author, Comments, Category, AudioURL, Length, Desc)
	return all_fields

""" Functions to generate an RSS feed file """

def print_header(f):
	f.write('<?xml version="1.0" encoding="utf-8"?>\n')
	f.write('<?xml-stylesheet type="text/css" href="css/main.css" media="screen"?>\n')
	f.write('<rss version="2.0">\n')
	f.write('  <channel>\n')

def print_title(f, title, link, description, meditor, webmaster, copy):
	f.write('    <generator>A RSS builder done by a little bit of magic in Python!</generator>\n')
	f.write('    <title>%s</title>\n' % title)
	f.write('    <link>%s</link>\n' % link)
	f.write('    <description>%s</description>\n' % description)
	f.write('    <language>en</language>\n')
	f.write('    <managingEditor>%s</managingEditor>\n' % meditor)
	f.write('    <webMaster>%s</webMaster>\n' % webmaster)
	f.write('    <copyright>Copyright 2015 by %s. All rights reserved.</copyright>\n' % copy)

def print_image(f, title, link, image):
	f.write('  <image>\n')
	f.write('    <title>%s</title>\n' % title)
	f.write('    <link>%s</link>\n' % link)
	f.write('    <url>%s</url>\n' % image)
	f.write('    <width>144</width>\n')
	f.write('    <height>144</height>\n')
	f.write('  </image>\n')

def print_entry(f, array):
	(Item, Title, PubDate, Links, Author, Comments, Category, AudioURL, Length, Desc) = array

	f.write('  <item>\n')
	f.write('    <title>%s</title>\n' % Title)
	f.write('    <pubDate>%s</pubDate>\n' % PubDate)
	f.write('    <link>%s</link>\n' % AudioURL)
	f.write('    <guid isPermaLink="true">%s</guid>\n' % AudioURL)
	f.write('    <description><![CDATA[%s]]></description>\n' % Desc)
	f.write('  </item>\n')

def print_footer(f):
	f.write('  </channel>\n')
	f.write('</rss>\n')


""" ***************  The Main Program begins here  *************** """

Today = time.time()

myAuthor = "David Billsbrough"
myEmail = "kc4zvw@147120.com"
myImage = "http://imglogo.podbean.com/image-logo/759672/DSCF0008.jpg"
myLink = "http://kc4zvw.strangled.net"
MyPodcast = "The Delta II Show"
SubTitle = "subtitle"
Webmaster = "webmaster@147120.com"
MaxPodcasts = 250

print
print "Read a text file of podcasting data (Python version)"
print
print "Today is %s (local)." % formattedDate(Today)
print


home = get_home_dir()

outfile = "delta2-podcasts.rss"
RSSFile = home + os.sep + outfile

third = ['/bin/cat', 'delta_podcast.txt']
fourth = ['./scan-delta-podcasts.awk']
p3 = subprocess.Popen(third, stdout=subprocess.PIPE)
p4 = subprocess.Popen(fourth, stdin=p3.stdout, stdout=subprocess.PIPE)
p3.stdout.close()  # Allow p3 to receive a SIGPIPE if p4 exits.
output = p4.communicate()[0]
output = string.rstrip(output)
alldata = string.split(output, "\n", MaxPodcasts)

try:
    report = open(RSSFile, 'w')
except IOError:
    print("Could not open %s for writing data." % RSSFile)
    sys.exit(1)

print_header(report)
print_title(report, MyPodcast, myLink, SubTitle, myAuthor, Webmaster, myAuthor)
print_image(report, 'Test title', myLink, myImage)

for aline in alldata:
	arecord = process_line(aline)
	(Item, Title, PubDate, Links, Author, Comments, Category, AudioURL, Length, Desc) = arecord
	print "Processing podcast number: %s" % Item
	display_line(arecord)
	print_entry(report, arecord)

print_footer(report)

report.close()

print
print("End of report")

sys.exit(0)

# End of script
