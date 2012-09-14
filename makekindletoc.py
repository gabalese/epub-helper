#! /usr/bin/env python3
# file: optimize.py
# Part of a larger helper script that minimizes manual intervention on ePubs exported from IDCS5.5
# Feel free to use, improve, insult or whatever. No credit required.

try:
	from lxml import etree as ET
except ImportError:
	print("REQUIRED: lxml library. Don't really know if the standard library xml.etree is equivalent")
	# Portability is not a matter of concern to me.
	# If you like to experiment, etree should be imported like:
	# import xml.etree.ElementTree as ET
	sys.exit(1)

# Namespaces shortcuts

NS_opf = "http://www.idpf.org/2007/opf"
NS_dc =	 "http://purl.org/dc/elements/1.1/"

	
def makeKindleTOC():
	"""Parses the toc.ncx file to build an elementary html toc"""
	
	opf = ET.parse("OEBPS/content.opf").getroot()
	reference = ET.SubElement(opf[3], "reference", attrib={"href":"toc.html", "type":"toc", "title":"toc.html"})
	opf[1].append(ET.Element("item",attrib={"href":"toc.html","id":"toc.html","media-type":"application/xhtml+xml"}))
	
	# We don't use a linked toc for general purpose ePub, so the toc.html won't be added to the spine.
	# The same item could be .append'ed to opf[2] if needed
	
	ncx = ET.parse("OEBPS/toc.ncx").getroot()
	
	list_a = []
	list_b = []
	text = ""
	text += """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<title>TOC</title>
		<link href="template.css" rel="stylesheet" type="text/css"/>
	</head>
	<body>""" # Yes, it's ugly. But it does work.
	
	cover =	opf.xpath("//d:reference[@title='Cover'] | //d:reference[@title='cover']",namespaces={"d":NS_opf})[0].get("href")
	
	text += '<p><a href="%s">%s</a>' % (cover,"Cover") + "</p>" + "\n"
	
	for navpoint in ncx[2]:
		list_a.append(navpoint[0][0].text)
		list_b.append(navpoint[1].get("src"))
		
	for a,b in zip(list_a, list_b):
		text += '<p><a href="%s">%s</a>' % (b,a) + "</p>" + "\n"
	
	text += "</body>" + "\n"
	text += "</html>" + "\n"	
	
	toc_html = open("OEBPS/toc.html","w")
	toc_html.write(text)
	toc_html.close()
	
	opf = ET.ElementTree(opf)
	opf.write("OEBPS/content.opf")
	
if __name__ == "__main__":
	makeKindleTOC()