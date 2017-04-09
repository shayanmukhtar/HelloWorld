#This script parses the output of KMP_A_DEBUG and try's to animate the sequence of task
#creation, stealing, and execution

import Tkinter as tk
from graphics import *

#Constant Data
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
HOR_OFFSET = 50
VER_OFFSET = 50
root = tk.Tk()

#Global variables
ThreadTaskHandles = [];
LabelTaskHandles = [];

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

#pass in the starting index of where the total number of threads would be
def getTotalNumThreadsString(string, index):
	returnValue = ""
	length = len(string)
	if ((index + 1) < length):
		#valid index, extract number (2 digits)
		returnValue = ConvertToInt(string[index:index+1])
	return returnValue

def getStdIntFromString(string, index, size):
	returnValue = ""
	length = len(string)
	if ((index + size) < length):
		returnValue = ConvertToInt(string[index:index+size])
	return returnValue

################ ANIMATION FUNCTIONS ############################
def pushTaskToDeque(currentThread, task):
	LabelTaskHandles[currentThread].append(ThreadTaskHandles[currentThread])
	LabelTaskHandles[currentThread][ThreadTaskHandles[currentThread]] = tk.Label(root, justify="center", text="Task " + str(task),bg="green", fg="black")
	LabelTaskHandles[currentThread][ThreadTaskHandles[currentThread]].grid(row = ThreadTaskHandles[currentThread] + 1, column=currentThread)	#+1 becaue first row taken by thread labels
	ThreadTaskHandles[currentThread] += 1
	#time.sleep(1)
	return

def stealTaskFromDeque(stealingThread, stolenThread, task):
	LabelTaskHandles[stolenThread][ThreadTaskHandles[stolenThread]-1].configure(bg="red", fg="black")
	try:
		input("Press enter to continue")
	except SyntaxError:
		pass
	pullTaskFromDeque(stolenThread, task)
	pushTaskToDeque(stealingThread, task)
	return

def pullTaskFromDeque(currentThread, task):
	LabelTaskHandles[currentThread][ThreadTaskHandles[currentThread]-1].destroy()
	LabelTaskHandles[currentThread].remove(LabelTaskHandles[currentThread][ThreadTaskHandles[currentThread]-1])
	ThreadTaskHandles[currentThread] -= 1
	#time.sleep(1)
	return

def executeTask(currentThread, task):
	LabelTaskHandles[currentThread][ThreadTaskHandles[currentThread]-1].configure(bg="yellow", fg="black")
	try:
		input("Press enter to continue")
	except SyntaxError:
		pass
	pullTaskFromDeque(currentThread, task)
	return

#################################################################
#	Setup the animation to use grid layout - begin reading		# 
#	in the log file and make some preliminary adjustments		#
#	based on number of threads									#
#################################################################

def runLogParser(logFile, outputLogfile):
	
	outString = ""
	outStringTaskSpawn = ""
	outStringTaskSpawnCurrent = ""

	

	#get the total number of threads in this implementation
	for currentLine in logFile:
		stringPosNumThreads = currentLine.find("Total Number of Shayan's Threads:")	
		if (stringPosNumThreads <> -1):
			totNumThreads = getTotalNumThreadsString(currentLine, stringPosNumThreads + 34)
			break

	threadList = [i for i in range(0,int(totNumThreads))]
	label = [i for i in range(0,int(totNumThreads))]
	for i in threadList:
		ThreadTaskHandles.append(0)
		LabelTaskHandles.append([])	#create a 2D array of labels - first dimension is thread number, second dimennsion is task
	threadWindowWidth = SCREEN_WIDTH / int(totNumThreads)
	####################Time to begin the animation of the OpenMP library#################################
	#first lets get some system information to display this properly


	root.resizable(width=False, height=False)
	root.geometry('{}x{}'.format(SCREEN_WIDTH + 2*HOR_OFFSET, SCREEN_HEIGHT + 2*VER_OFFSET))
	root.wm_title("Fibonacci Sequence Task Execution")
	#win = GraphWin('Fibonacci Sequence Task Execution', SCREEN_WIDTH + 2*HOR_OFFSET, SCREEN_HEIGHT + 2*VER_OFFSET) # give title and dimensions
	#lets assume useable space in the windows is SCREEN_WIDTH x SCREEN_HEIGHT - all edges are trailed by *_OFFSET

	#lets not worry about running out of height yet //TODO
	for i in threadList:
		threadList[i] = i*threadWindowWidth + HOR_OFFSET
		label[i] = tk.Label(root, justify="center", text="Thread " + str(i))
		label[i].grid(row = 0, column=i)
		root.grid_columnconfigure(i, minsize=threadWindowWidth)

	for currentLine in logFile:
		root.update()
		#time.sleep(0.0004)
		#parse the log file portion containing push task to deque
		stringPosThreadPushTask = currentLine.find("TASK_SUCCESSFULLY_PUSHED: ")	
		if (stringPosThreadPushTask <> -1):
			currentThread = getStdIntFromString(currentLine, len("__kmp_push_task: T#"), 2)
			stringPosGTID = currentLine.find("My_GTID = ");
			currentTask = getStdIntFromString(currentLine, stringPosGTID + len("My_GTID = ") - 1, 3)
			outputLogfile.write("Thread " + currentThread + " creates task " + currentTask + "\n")
			pushTaskToDeque(int(currentThread),int(currentTask))
			try:
				input("Press enter to continue")
			except SyntaxError:
				pass
	
		#parse the log file portion that contains task stealing
		stringPosStealTask = currentLine.find("__kmp_steal_task(exit #3): ")
		if (stringPosStealTask <> -1):
			currentThread = getStdIntFromString(currentLine, len("__kmp_steal_task(exit #3): T#"), 2)
			stringPosStolenTaskID = currentLine.find("My_GTID = ")
			stolenTaskID = getStdIntFromString(currentLine, stringPosStolenTaskID + len("My_GTID = ") -1, 3)
			stringPosStolenThread = currentLine.find("from T#")
			stolenThreadID = getStdIntFromString(currentLine, stringPosStolenThread + len("from T#"), 2)
			outputLogfile.write("Thread " + currentThread + " stole task " + stolenTaskID + " from thread " + stolenThreadID + "\n")
			stealTaskFromDeque(int(currentThread), int(stolenThreadID), int(stolenTaskID))
			try:
				input("Press enter to continue")
			except SyntaxError:
				pass

		#parse the log file portion containing task execution
		stringPosStartTask = currentLine.find("__kmp_task_start(enter): T#")
		if (stringPosStartTask <> -1):
			currentThread = getStdIntFromString(currentLine, len("__kmp_task_start(enter): T#"), 2)
			stringPosStartTask = currentLine.find("New Tasks My_GTID = ")
			startTask = getStdIntFromString(currentLine, stringPosStartTask + len("New Tasks My_GTID = ") - 1, 3)
			outputLogfile.write("Thread " + currentThread + " begins executing task " + startTask + "\n")
			executeTask(int(currentThread),int(currentTask))
			try:
				input("Press enter to continue")
			except SyntaxError:
				pass
	outputLogfile.write("Total threads were: " + totNumThreads)
	return

#################################################################
#	Run all the closing tasks									#
#################################################################
def closeOut(logFile, outputLogfile):
	root.destroy()
	#close file at the end
	logFile.close()
	outputLogfile.close()
#################################################################
#	MAIN														#
#################################################################
def main():
	logFile = open("test.txt","r")
	outputLogfile = open("testingScript.txt","w")
	runLogParser(logFile, outputLogfile)
	closeOut(logFile, outputLogfile)
	return

#lets go
main()



