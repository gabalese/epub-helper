#! /usr/bin/env python3
# file: cssstylelist.py
# Make a list of every style used in html and returns that
# From the CLI, type `./cssstylelist.py > file_with_a_list.txt
# Feel free to address any complain to @gabalese

import os, glob, sys
try:
	from lxml import etree as ET
except ImportError:
	import xml.etree.ElementTree as ET
	print("lxml not installed. Running with xml.etree instead")

path = "OEBPS/Text" # your mileage may vary
list = []
new_list = []

def cssList():
	global list
	global new_list 
	for infile in glob.glob(os.path.join(path, '*html')):
		try:
			html = ET.parse(infile).getroot()
		except:
			print("ERROR: Unable to parse " + infile)
			print("This is likely to happen with ill-formed xhtml files.")
			sys.exit(1)
		for i in html.iter():
			list.append(i.get("class"))
	
	for i in list:
		if i not in new_list:
			if i is not None:
				new_list.append(i)
			
	return new_list	


	
if __name__ == "__main__":
	for item in (cssList()):
		print(item)