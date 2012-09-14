#! /usr/bin/env python3
# Extracts the (x)html contents of an epub file, numbered according to the spine order

from lxml import etree as ET
import zipfile as ZIP
import sys
import os
import shutil

namespaces = {"opf":"http://www.idpf.org/2007/opf","dc":"http://purl.org/dc/elements/1.1/"}
root_folder = ''
epubtitle = ''
info = {}

def parseInfo(file):
    
    global root_folder
    global epubtitle
    global info
    
    try:
        f = ET.fromstring(ZIP.ZipFile(file).read("META-INF/container.xml"))
        info["path_to_opf"] = f[0][0].get("full-path")
        root_folder = os.path.dirname(info["path_to_opf"])
    except Exception as e:
        print("Something went horribly wrong!!! ", e)

    opf = ET.fromstring(ZIP.ZipFile(file).read(info["path_to_opf"]))
    
    id = opf.xpath("//opf:spine",namespaces=namespaces)[0].get("toc")
    expr = "//*[@id='%s']" % id
    info["ncx_name"] = opf.xpath(expr)[0].get("href")
    epubtitle = opf.xpath("//dc:title",namespaces=namespaces)[0].text
    epubtitle = epubtitle.replace(" ","")

    return info

if __name__ == '__main__':
	file = sys.argv[1]
	info = parseInfo(file)
	opf = ET.fromstring(ZIP.ZipFile(file).read(info["path_to_opf"]))
	manifest = opf[1]
	spine = opf[2]

	orderedlist = []
	
	for num,i in enumerate(spine):
		idref = i.get("idref")
		expr = "//*[@id='%s']" % str(idref)
		href = opf.xpath(expr)[0].get("href")
		orderedlist.append(href)
	
	for num , f in enumerate(orderedlist):
			ZIP.ZipFile(file).extract(root_folder+"/"+f)
			os.rename(root_folder + "/" + f, "%s_%05d.html" % (epubtitle,num))
	shutil.rmtree(root_folder)