from subprocess import Popen, PIPE, check_output
import os, fnmatch
import time 
import xml.etree.ElementTree as ET

def runFlowDroid():

    """
        Code runs FlowDroid as per given instructions. Commands are wired inside the method. The apk files (entire set of 3k apps)
        are downloaded already and are available in the folder as mentioned in the commands. An improvement and future work could
        be making REST calls to get the .apk s dynamically from the dataset site.

        Code has security issues while using inbuilt ElementTree and subprocess (shell = True)
        [sending a malicious modified xml in ElementTree, shell injection attacks]
        !!! DO NOT USE THIS CODE OUTSIDE YOUR LAPTOP !!! or if you dont have control over your xml files.

        input: Takes no argument
        returns a list containing 2 values - [ files processed , number of files skipped ]
    """
    
    count = 0
    skipped = 0
    listOfFiles = os.listdir('/Users/prashanthikanniapanmurthy/Desktop/Fall18/CNS/proj4/testAPIS/playdrone-apk-c7/')  #playdrone-apk-c7/
    pattern = "*.apk"  
    cmd1 = "java -Xms2048m -jar soot-infoflow-cmd/target/soot-infoflow-cmd-jar-with-dependencies.jar -a /Users/prashanthikanniapanmurthy/Desktop/Fall18/CNS/proj4/testAPIS/playdrone-apk-c7/" #playdrone-apk-c7/
    cmd2 = " -p /Users/prashanthikanniapanmurthy/Library/Android/sdk/platforms  -s ./soot-infoflow-android/SourcesAndSinks.txt -out "
    for entry in listOfFiles: 
            if fnmatch.fnmatch(entry, pattern) and count < 50:
                
                print("Running .....", end=" ")
                print (entry)
                os.chdir("/Users/prashanthikanniapanmurthy/Desktop/Fall18/CNS/proj4/FlowDroid")
                output_file = "/Users/prashanthikanniapanmurthy/Desktop/Fall18/CNS/proj4/OutFiles/"+entry+"_out.xml"
                extensions = "" # for adding any other options for performance
                cmd = cmd1+entry+cmd2+output_file+extensions
                rm_cmd = "rm "+output_file
                print (cmd)
                try :
                    output = check_output(cmd, timeout=(60*15), shell=True) #Timing out after 15 mintutes
                except :
                    print ("Timed out ... Moving on to next file ")
                    skipped+=1
                    continue
                if ( leaksinApps(output_file) == 0 ):
                    skipped +=1
                count +=1
                
    return [count,skipped]

def leaksinApps(xml):
    """
    Method returns the leakages in the apk file. Counts the number of sink tags in the parsed xml

    input: takes the xml file as an argument
    returns the number of leakages
    """
    tree = ET.parse(xml)
    root = tree.getroot()
    leaks = 0 
    for Sink in root.iter('Sink'):
        leaks+=1
    return leaks

start_time = time.time()
output_list = runFlowDroid()
print ("Total Files : ",output_list[0])
print ("Skipped Files : ",output_list[1])
print ("total time taken for the code to finish (in mins): ",(time.time() - start_time)/60)