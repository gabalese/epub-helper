#! /usr/bin/env python3
# file: cssstylelist.py
# Make a list of every style used in html and print to stdout

import os, glob, sys
import zipfile as ZIP
from lxml import etree as ET

try:
	from lxml import etree as ET
except ImportError:
	print("lxml not installed.")
	sys.exit()

list = []
new_list = []
filelist = []
root_folder = ""
namespaces = namespaces = {"opf":"http://www.idpf.org/2007/opf","dc":"http://purl.org/dc/elements/1.1/"}

def cssList(infile):
	global list
	global new_list 
	# init a tolerant parser
	parser = ET.HTMLParser()
	html = ET.fromstring(infile,parser)
	
	for i in html.iter():
		list.append(i.get("class"))


def parseInfo(file):
	info = {}
	global root_folder
	try:
		f = ZIP.ZipFile(file).read("META-INF/container.xml")
	except KeyError:
		print( "The %s file is not a valid OCF." % str(file) )
	try:
		f = ET.fromstring(f)
		info["path_to_opf"] = f[0][0].get("full-path")
		root_folder = os.path.dirname(info["path_to_opf"])
	except:
		pass
	opf = ET.fromstring(ZIP.ZipFile(file).read(info["path_to_opf"]))
	
	id = opf.xpath("//opf:spine",namespaces=namespaces)[0].get("toc")
	expr = "//*[@id='%s']" % id
	info["ncx_name"] = opf.xpath(expr)[0].get("href")
	info["path_to_ncx"] = root_folder + "/" + info["ncx_name"]
	info.pop("ncx_name")
	return info
	
def parseOPF(file):
	meta = {}
	opf = ET.fromstring(ZIP.ZipFile(file).read(parseInfo(file)["path_to_opf"]))
	
	return opf



if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("USAGE: \
		./cssstylelist.py <epubfile>")
		sys.exit()
		
	i = sys.argv[1]
	opf = parseOPF(i)
	for item in opf.xpath("//opf:item",namespaces=namespaces):
		if item.get("media-type") == "application/xhtml+xml":
			filelist.append(item.get("href"))
	
	for item in filelist:
		cssList(ZIP.ZipFile(sys.argv[1]).read(root_folder+"/"+item))
	
	for i in list:
		if i not in new_list:
			if i is not None:
				new_list.append(i)
	
	for i in new_list:
		print(i)