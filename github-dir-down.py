import requests
import os

def clone_dir(contents,align,apiurl):
	for content in contents.json():
		#if directory download its content recursively
		if content['type'] == 'dir':
			apiurl = apiurl + "/" + content['name']
			contents = requests.get(apiurl)

			parentdir = os.getcwd()
			os.makedirs(content['name'])
			os.chdir(content['name'])
			clone_dir(contents,align+1,apiurl)
			os.chdir(parentdir)
		#if file write it
		else:
			fh = open(content['name'],'w')
			rawfile = requests.get(content['download_url'])
			fh.write(rawfile.content)
			fh.close()

#it works only for folders with https://github.com/:user/:repo/tree/master/:path
path = raw_input("Path to clone")
args = path.split('/',7)
apiurl = "https://api.github.com/repos/" + args[3] + "/" + args[4] + "/contents/" + args[7]
contents = requests.get(apiurl)

clone_dir(contents,0,apiurl)