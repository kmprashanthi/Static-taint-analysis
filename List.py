from subprocess import Popen, PIPE, check_output
import os, fnmatch
import time 
import xml.etree.ElementTree as ET

def leaksinApps(xml):
    tree = ET.parse(xml)
    root = tree.getroot()
    leaks = 0 
    for Sink in root.iter('Sink'):
        leaks+=1
    return leaks

count = 0
leakN = 0
listOfFiles = os.listdir('/Users/prashanthikanniapanmurthy/Desktop/Fall18/CNS/proj4/Outfiles/')
pattern = "*.xml" 
for entry in listOfFiles:
    if fnmatch.fnmatch(entry, pattern):
        count+=1
        print ("Printing ....... ",entry)
        xmlfile = "/Users/prashanthikanniapanmurthy/Desktop/Fall18/CNS/proj4/Outfiles/" +entry
        leak = leaksinApps(xmlfile)
        if leak == 0:
            leakN+=1
        with open("Entries.txt", "a") as names:
            names.write(entry+" "+str(leak)+'\n')
       