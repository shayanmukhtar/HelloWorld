#This script parses the output of KMP_A_DEBUG and figures out which tasks spawn which tasks
#it doesnt do the deque animation (yet :))

#take an arbitary string and return whether or not it represents a valid integer
def isValidInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

#take an arbitrary string and drop all non-integer components of it
def ConvertToInt(string):
	returnValue = ""
	for currentChar in string:
		if isValidInt(currentChar):
			returnValue = returnValue + currentChar
	return  returnValue

#pass in the starting index of where the GTID would be as index
def GetTaskIDString(string, index):
	returnValue = ""
	length = len(string)
	if ((index + 2) < length):
		#valid index, extract number (3 digits)
		returnValue = ConvertToInt(string[index:index+3])
	return returnValue

#pass starting index of "PAPI Information"
def GetPAPIInformation(string, index):
	returnValue = ""
	returnValue = string[index + len("PAPI Information:"):]
	CyclePos = returnValue.find("Cycles:")
	L1Pos = returnValue.find("L1 Misses:")
	returnValue = returnValue[0:CyclePos-1] + "\n" + returnValue[CyclePos:L1Pos-1] + "\n" + returnValue[L1Pos:]
	return returnValue



logFile = open("test.txt","r")
outString = ""
outStringTaskSpawn = ""
outStringTaskSpawnCurrent = ""

for currentLine in logFile:
	stringPosPTID = currentLine.find("Parents Task My_GTID")	
	if (stringPosPTID <> -1):
		stringPosCID = currentLine.find("New Tasks My_GTID")
		#outStringTaskSpawn = currentLine[(stringPosPTID + 22):(stringPosPTID + 25)]
		#form single line relationship between parent task and child task
		outStringTaskSpawnCurrent = "T" + GetTaskIDString(currentLine,stringPosPTID + 23)
		outStringTaskSpawnCurrent += " -> "
		outStringTaskSpawnCurrent +=  "T" + GetTaskIDString(currentLine,stringPosCID + 20) + " "
		PapiString = GetPAPIInformation(currentLine, currentLine.find("PAPI Information"))
		outStringTaskSpawnCurrent += "[label = \"" + PapiString + "\"]"
		outStringTaskSpawnCurrent += ";\n"
		outStringTaskSpawn += "\t" + outStringTaskSpawnCurrent

#create the output DOT graph
outputLogfile = open("taskSpawn.dot","w")
outputLogfile.write("//task spawn graph\n")
outputLogfile.write("digraph taskSpawn {\n")
outputLogfile.write(outStringTaskSpawn)
outputLogfile.write("\n")
outputLogfile.write("}")

#close file at the end
logFile.close()
outputLogfile.close()




