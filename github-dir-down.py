import requests
import os

def clone_dir(align,apiurl):
	contents = requests.get(apiurl)

	for content in contents.json():
		#if directory download its content recursively
		if content['type'] == 'dir':
			for i in range(align):
				print "-",
			print content['name']

			parentdir = os.getcwd()
			os.makedirs(content['name'])
			os.chdir(content['name'])
			clone_dir(align+1,apiurl + "/" + content['name'])
			os.chdir(parentdir)
		#if file write it
		else:
			for i in range(align):
				print "-",
			print content['name']
			fh = open(content['name'],'w')
			rawfile = requests.get(content['download_url'])
			fh.write(rawfile.content)
			fh.close()

#it works only for folders with https://github.com/:user/:repo/tree/master/:path
path = raw_input("Path to clone : ")
args = path.split('/',7)
apiurl = "https://api.github.com/repos/" + args[3] + "/" + args[4] + "/contents/" + args[7]
os.makedirs(args[7])
os.chdir(args[7])
print "Below files/directories are cloned"
clone_dir(0,apiurl)
print "Completed"