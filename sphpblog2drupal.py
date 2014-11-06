#!/usr/bin/env python
# MODIFY THESE SETTINGS FOR YOUR sphpblog INSTALL
sphpblogBaseDir="/var/www/vhosts/example.com/htdocs"

# MODIFY THESE SETTINGS FOR YOUR drupal INSTALL
drupalUser="admin"
drupalPass="somepass"
drupalDB="example_drupal52"
ownerUID=2

# You'll probably want to leave everything below this line alone unless
# you'd like to know how the program works.
#
# Copyright leo@raeleo.com 2007 under the GNU GPL
#
import re
import os
import sys
import MySQLdb

sphpblogContentBaseDir=sphpblogBaseDir + "/content"

def importEntries(contentFile):
	f=open(contentFile, 'r')
	file=f.read()
	f.close()
	entries=file.split("VERSION|")
	for entry in entries:
        	row=entry.split("|")
        	if(len(row) > 1):
			pat=re.compile(r'.*?/entry')
			fileTmp=pat.sub('',contentFile)
			pat=re.compile(r'-.*?$')
			fileDate=pat.sub('',fileTmp)
			year="20" + fileDate[:2]
			month=fileDate[2:4]
			day=fileDate[4:]
			date=month + "-" + day + "-" + year
                	subj=row[2].replace("&quot;","\"").replace("&lt;","<").replace("&#039;","'").replace("&gt;",">").replace("&amp;","&")
                	bodyAsLines = row[4].splitlines()

                	bodyHTML = ""
                	for line in bodyAsLines:
                        	#FIXME -- only allows one image per line
                        	# in my blog I only have one image per line
				line.rstrip()
                        	if(re.search('\[img=.*?\]',line)):
                                	imgLine=line.split('[img=images/')
                                	afterImg=imgLine[1]
                                	pat=re.compile(r'\s.*?\]')
                                	imgEndLine=pat.split(afterImg)
					newLine=imgLine[0] + "<img src=/files/" + imgEndLine[0] + ">" + imgEndLine[1] + "\n"
                                	bodyHTML+= newLine
                        	elif(line != ''):
                                	bodyHTML+= line.replace("&quot;","\"").replace("&lt;","<").replace("&#039;","'").replace("&gt;",">").replace("&amp;","&") + "\n"

			timeS=row[len(row)-1]
			return(int(timeS),subj,bodyHTML)

def contentFileList(sphpblogBaseDir):
	cFL=[]
	for root,dirs,filelist in os.walk(sphpblogContentBaseDir):
		for file in filelist:
			if( re.search('^entry.*?\.txt$',file) ):
				cFL.append( (os.path.join(root,file),file.replace(".txt","")) )
	return(cFL)

def drupalEntryAdd(db,uid,entry,oldPageName):
	c=db.cursor()

	# add node for blog entry
	timeS=entry[0]
	subj=entry[1].replace('\'','\\\'')
	add_node="insert into node (type,title,uid,status,created,changed,comment,promote,moderate,sticky) values ('blog','%s',%d,1,%d,%d,2,1,0,0);" % (subj,ownerUID,timeS,timeS)
	c.execute(add_node)

	get_last_nid="select last_insert_id();"
	c.execute(get_last_nid)
	last_nid=c.fetchone()
	update_last_node="update node set vid=%d where nid=%d;" % (last_nid[0],last_nid[0])
	c.execute(update_last_node)

	# add contents for post
	body=entry[2].replace('\'','\\\'')
	teaser=body[0:320] # give first 99 chars as teaser
	# the following makes the node in the "Full HTML" format to allow
	# images
	add_node_revisions="insert into node_revisions (nid,vid,uid,title,teaser,body,log,timestamp,format) values (%d,%d,%d,'%s','%s','%s','%s',%d,3);" % (last_nid[0],last_nid[0],ownerUID,subj,teaser,body,oldPageName,timeS)
	c.execute(add_node_revisions)

# MAIN
print "This script was tested on ONE install of sphpblog and ONE install of Drupal 5.2.  If you want to continue you do so at your own risk."
print "***This script is realeased AS-IS with no warranty under the GNU GPL.***"
print "***Test this out on a test Drupal install with a test database before trying it on a live web site!!!***"
print ""
print "Proceed with the following settings?"
print "blog entry \"Input format\" Full HTML"
print "sphpblog install located at: %s" % sphpblogBaseDir
print "drupal user to own blog entries: %s" % ownerUID
print "mysql db: %s" % drupalDB
print "mysql user: %s" % drupalUser
print "mysql pass: %s" % drupalPass
print ""
print "Continue? (Yes/No)"
if(sys.stdin.readline().rstrip() == "Yes"):
	print "Continuing..."
else:
	print "Good plan.  Test thoroughly first."
	sys.exit()

db=MySQLdb.connect(user=drupalUser,passwd=drupalPass,db=drupalDB)
count=0
log=[]
for file in contentFileList(sphpblogBaseDir):
	log.append(file[0] + "\n")
	drupalEntryAdd(db,ownerUID,importEntries(file[0]),file[1])
	count = count + 1

log.append("Imported %d entries.\n" % (count))
log.append("\n")
log.append("Don't forget:\n")
log.append("*your static pages\n")
log.append("*copy your images from your sphpblog's base /images directory to your Drupal /files directory\n")
log.append("Good luck!\n")
f=open("sphpblog-migrate.log", 'w')
file=f.writelines(log)
f.close()
for line in log:
	print line.rstrip()

