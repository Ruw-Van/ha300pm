# coding: utf-8

import sys
import os
import urllib2
import datetime
# import locale


if __name__ == "__main__":
	if(len(sys.argv) != 2):
		print u"Err!\n\tCommand: python dac-ha300-playlist-maker [DirectoryPath]"
		sys.exit()

	target = sys.argv[1]
	if not os.path.isdir(target):
		print u"Err!\n\tCommand: python dac-ha300-playlist-maker [DirectoryPath]"
		sys.exit()

	if target[-1:] != "/":
		target = target + '/'

	filelist = []
	extlist = [ ".mp3", ".wma", ".wav", ".aac", ".m4a", ".mp4", ".flac", ".dsf", ".dff" ]
	for root, dirs, files in os.walk(target):
		for file in files:
			# print os.path.realpath(os.path.join(root, file))
			# print os.path.splitext(os.path.realpath(os.path.join(root, file)))[1]
			if file[0] == ".":
				continue
			if os.path.splitext(file)[1] in extlist:
				filelist.append(target+file)

	if filelist < 1:
		print u"Err!\n\tFile not Found!"
		sys.exit()

	PlayListFileName = os.path.split(os.path.dirname(target))[1] + ".xml"

	# XML構築するよ
	PlaylistItems = []
	TracksItems = []
	PlaylistItem = 	'''				<dict>
					<key>Track ID</key>
					<integer>%d</integer>
				</dict>'''
	TracksItem = '''	<dict>
		<key>%d</key>
		<dict>
			<key>Artist</key>
			<string></string>
			<key>Location</key>
			<string>file://localhost%s</string>
			<key>Name</key>
			<string></string>
			<key>Optional Duration Time</key>
			<integer>0</integer>
			<key>Optional Offset Time</key>
			<integer>0</integer>
			<key>Track ID</key>
			<integer>%d</integer>
		</dict>
	</dict>'''

	TrackID = 0
	for file in filelist:
		# print "file://localhost" + urllib2.quote(os.path.realpath(file))
		TrackID += 1
		PlaylistItems.append( PlaylistItem % TrackID)
		TracksItems.append( TracksItem % (TrackID, urllib2.quote(file), TrackID) )

	# print "\n".join(TracksItems)

	xml = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Playlists</key>
	<array>
		<dict>
			<key>Playlist Items</key>
			<array>
%s
			</array>
		</dict>
	</array>
	<key>Tracks</key>
%s
</dict>
</plist>''' % ("\n".join(PlaylistItems), "\n".join(TracksItems))

	# 上書き防止
	if os.path.isfile(PlayListFileName):
		os.rename(PlayListFileName, PlayListFileName+"."+datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
	
	f = open(PlayListFileName, 'w')
	f.write(xml)
	f.close()
	os.utime(PlayListFileName, None)

