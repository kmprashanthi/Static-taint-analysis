import xml.etree.ElementTree as ET
from subprocess import Popen, PIPE, check_output
import os, fnmatch

def parseXML(xmlfile,App):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    leaks = 0
    sources = App
    sinks = App
    sink = ''
    source = ''

    for ele in root.iter('Sink'):
        leaks+=1
        for key,val in ele.attrib.items():
            if key == 'Statement':
                sink = sink + '||Sink Statement||' + val
            if key == 'Method':
                sink = sink + '||Sink Method:||'+val

    for ele in root.iter('Source'):
        for key,val in ele.attrib.items():
            if key == 'Statement':
                source = source + '||Source Statement:||'+val
            if key == 'Method':
                source = source + '||Source method:||'+ val

    sinks = sinks + sink + "\n"
    sources = sources + source + "\n"

    with open("Sinks.log", "a") as sinkfile:
        sinkfile.write(sinks)

    with open("Sources.log", "a") as sourcefile:
        sourcefile.write(sources)

count = 0
listOfFiles = os.listdir('/Users/prashanthikanniapanmurthy/Desktop/Fall18/CNS/proj4/Outfiles/')
pattern = "*.xml" 
for entry in listOfFiles:
    if fnmatch.fnmatch(entry, pattern) :
        count+=1
        print ("Printing ....... ",entry)
        xmlfile = "/Users/prashanthikanniapanmurthy/Desktop/Fall18/CNS/proj4/Outfiles/" +entry
        parseXML(xmlfile,str(entry))
        print ("done parsing : ",entry)