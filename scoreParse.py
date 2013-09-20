from __future__ import division
import csv
import re
import os


dir = os.path.dirname(__file__)
logFile = os.path.join(dir, 'sqlout.csv')
logFile2 = os.path.join(dir, 'out2.csv')

#validNames = {'cody': (0,0), 'cory': (0,0), 'cory1': (0,0), 'daniel': (0,0), 'nate': (0,0), 'chris': (0,0), 'cordy': (0,0), 'anu': (0,0), 'ian': (0,0), 'amanda': (0,0), 'mike': (0,0) }
#nameLookups = {'cody': ['cody.hard'], 'daniel': ['daniel.plemmons'], 'nate': ['nathaniel.m.ford', 'nford.zynga'], 'chris': ['cosberg_zynga'], 'anu': ['asrivas.zynga'], 'mike': ['mrmkenyon', 'mkenyonzynga'], 'ian': ['ian.guthridge'], 'amanda': ['amanda.schloss']}
nameLookup = {'cody.hard': 'cody', 'daniel.plemmons': 'daniel', 'nathaniel.m.ford': 'nate', 'nford.zynga': 'nate', 'cosberg_zynga': 'chris', 'asrivas.zynga': 'anu', 'mrmkenyon': 'mike', 'mkenyonzynga': 'mike', 'ian.guthridge': 'ian', 'amanda.schloss': 'amanda'}

scores = {}
authors = {}

class User:
	def __init__(self):
		self.postCount = 0
		self.pointsGiven = 0
		self.pointsTaken = 0
		self.pointsRecieved = 0
		self.pointsDeducted = 0
		self.rawPositives = []
		self.rawNegatives = []



def readLogs():
	#csvReader =  csv.DictReader(open(logFile))
	#seachForPoints(csvReader)
	csvReader =  csv.DictReader(open(logFile2))
	seachForPoints(csvReader)
	generateScores()
	#nameTuples = list()

	authList = authors.items()
	authList = sorted(authList, key= lambda authKey: authKey[1].pointsRecieved - authKey[1].pointsDeducted, reverse=True)
	print "(sun) Scores (sun)"

	for authItem in authList:
		pointsTotal = authItem[1].pointsRecieved - authItem[1].pointsDeducted
		mPM = round((pointsTotal*1000) / authItem[1].postCount,2)
		ptsGiven = authItem[1].pointsGiven
		ptsTaken = authItem[1].pointsTaken
		print `authItem[0]` + ": " + `pointsTotal` + " | mP/M: " + `mPM` + " | generosity: " + `ptsGiven` + " | malevolence: " + `ptsTaken`

	
	#for nameTup in nameTuples:
	#	if nameTup[2] != 0:
	#		print `nameTup[0]` + ": " + `nameTup[1]` + " | mP/M: " + `round((nameTup[1]*1000)/nameTup[2], 2)` + " | Given: " + `nameTup[3]`
	#	else:
	#		print `nameTup[0]` + ": " + `nameTup[1]` + " | Given: " + `nameTup[3]`

def generateScores():
	for author in authors.keys():
		#print author
		#print authors[author].rawPositives
		for point in authors[author].rawPositives:
			nameFind = re.findall('[a-zA-Z]+', point)
			
			for name in nameFind:
				if name in authors.keys():
					authors[name].pointsRecieved += 1
					authors[author].pointsGiven += 1
					#print "point: " + `point` + " from: " + `author` + " to: " + `name` + " rec: " + `authors[name].pointsRecieved` + " giv: " + `authors[author].pointsGiven`

		for point in authors[author].rawNegatives:
			nameFind = re.findall('[a-zA-Z]+', point)
			
			for name in nameFind:
				if name in authors:
					#print "deduction: " + `point` + " from: " + `author`
					authors[name].pointsDeducted += 1
					authors[author].pointsTaken += 1

def seachForPoints(reader):
	qid = 0
	for row in reader:
		author = None
		if row["author"] in nameLookup.keys():
			authorName = nameLookup[row["author"]]
		else:
			continue

		if authorName in nameLookup.values():
			if authorName not in authors.keys():
				author = User()
				author.postCount += 1
				authors[authorName] = author
			else:
				author = authors[authorName]
				author.postCount += 1

		testString = str(row["body_xml"])

		res = re.findall('[a-zA-Z]{2,}\s*\+\+', testString)
		#print `authorName` + " author[authorName]" + `authors[authorName]`
  		if len(res) > 0:
			for match in res:
				authors[authorName].rawPositives.append(str(qid) + "-" + match.lower())
				#print `qid` + " " + `authorName` + " - " + testString
				qid+=1
				
				#pos_results.append((match.lower(), row["author"]))
 
		res = re.findall('\+\+\s*[a-zA-Z]{2,}', testString)
		if len(res) > 0:
			for match in res:
				authors[authorName].rawPositives.append(str(qid) + "-" + match.lower())
				#print `qid` + " " + `authorName` + " - " + testString
				qid+=1
				
				#pos_results.append((match.lower(), row["author"]))
 
		res = re.findall('[a-zA-Z]{2,}\s*--', testString)
		if len(res) > 0:
			for match in res:
				authors[authorName].rawNegatives.append(str(qid) + "-" + match.lower())
				#print `qid` + " " + `authorName` + " - " + testString
				qid+=1
				
				#neg_results.append((match.lower(), row["author"]))
 
		res = re.findall('--\s*[a-zA-Z]{2,}', testString)
		if len(res) > 0:
			for match in res:
				authors[authorName].rawNegatives.append(str(qid) + "-" + match.lower())
				#print `qid` + " " + `authorName` + " - " + testString
				qid+=1
				
				#neg_results.append((match.lower(), row["author"]))



if __name__ == "__main__":
	readLogs()