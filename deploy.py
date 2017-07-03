#!/usr/bin/python
#coding:utf-8

import ftplib
import multiprocessing 
import os
import sys


dir = sys.argv[1]

def run():
#	hosts = [""]

	hosts = ["127.0.0.1"]
	send_to_hosts(hosts)



def send_to_hosts(hosts):
	processes = []
	for host in hosts:
		process = multiprocessing.Process(target=send, args=(host,))
		processes.append(process)
		process.start()

	for process in processes:
		process.join()
	

def send(host):
	ftp = ftplib.FTP()
	ftp.connect(host, 21, 60)
	ftp.login('user', 'passwd')
	sendfiles(ftp)


	ftp.quit()
	ftp.close()

def sendfiles(ftp):

	#ftp.mkd('cloudNew_20161010')
	ftpmkdir(ftp, dir, True)
	for filepath in walk_tree_files(dir):
		f = open(filepath, 'rb')
		#ftp.storbinary('STOR cloudNew_20161010/%s' % os.path.basename(filepath), f)
		#print os.path.dirname(filepath)
		ftpmkdir(ftp, os.path.dirname(filepath), True)
		#ftp.storbinary('STOR cloudNew_20161010/%s' % filepath, f)
		ftp.storbinary('STOR %s' % filepath, f)
		f.close()
		

def walk_tree_files(dir):
    if dir and os.path.isdir(dir):
        for root, dirs, files in os.walk(dir):
            for name in files:
                yield os.path.join(root, name)


def ftpmkdir(ftp, dir, first):
	try:
		ftp.mkd(dir)
	except Exception, e:
		print e,dir
		head,tail = os.path.split(dir)
		if len(head) != 0 and first == True:
			ftpmkdir(ftp, head, True)
			ftpmkdir(ftp, dir, False)

if __name__ == '__main__':	
	if len(sys.argv) < 2 :
		sys.exit()


	try:
		run()
	except Exception, e:
		print e
		sys.exit()
