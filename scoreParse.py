import csv
import re
import os


dir = os.path.dirname(__file__)
logFile = os.path.join(dir, 'sqlout.csv')
logFile2 = os.path.join(dir, 'out2.csv')

validNames = ['cody','cory', 'cory1', 'daniel','nate','chris','cordy', 'anu','ian','amanda','mike']

pos_results = list()
neg_results = list()
scores = {}
nameTuples = list()

def readLogs():
	csvReader =  csv.DictReader(open(logFile))
	seachForPoints(csvReader)
	csvReader =  csv.DictReader(open(logFile2))
	seachForPoints(csvReader)
	
	generateScores()
	nameTuples = list()

	print "Scores"
	for key in scores.keys():
		if key in validNames:
			nameTuples.append((key, scores[key]))

	#print "\nINVALID KEYS"
	#for key in scores.keys():
	#	if key not in validNames:
	#		print `key` + ": " + `scores[key]`

	nameTuples = sorted(nameTuples, key= lambda nameTup: nameTup[1], reverse=True)

	for nameTup in nameTuples:
		print `nameTup[0]` + ": " + `nameTup[1]`

def generateScores():
	for point in pos_results:
		nameFind = re.findall('[a-zA-Z]+', point)
		
		for name in nameFind:
			if name not in scores:
				scores[name] = 1
			else:
				scores[name]+=1

	for point in neg_results:
		nameFind = re.findall('[a-zA-Z]+', point)
		
		for name in nameFind:
			if name not in scores:
				scores[name] = -1
			else:
				scores[name]-=1

def seachForPoints(reader):
	for row in reader:
		testString = str(row["body_xml"])
		#if "++" in testString:
		#	print testString
		res = re.findall('[a-zA-Z]{2,}\s*\+\+', testString)
  		if len(res) > 0:
			for match in res:
				pos_results.append(match.lower())
 
		res = re.findall('\+\+\s*[a-zA-Z]{2,}', testString)
		if len(res) > 0:
			for match in res:
				pos_results.append(match.lower())
 
		res = re.findall('[a-zA-Z]{2,}\s*--', testString)
		if len(res) > 0:
			for match in res:
				neg_results.append(match.lower())
 
		res = re.findall('--\s*[a-zA-Z]{2,}', testString)
		if len(res) > 0:
			for match in res:
				neg_results.append(match.lower())

if __name__ == "__main__":
	readLogs()