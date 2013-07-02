import urllib2
import json
from flask import escape
from app import app
import datetime,math

class dataController:
	def compareTweetCount(_self,user1,user2,duration):
		data1=_self.getData(user1,int(duration)-1)
		data2=_self.getData(user2,int(duration)-1)
		json=_self.generateJSON(data1,data2,int(duration),user1.encode('ascii','ignore'),user2.encode('ascii','ignore'))
		return json
	
	#Function to fetch tweets in time span of 'duration'
	def getData(_self,user,duration):
		data=[]
		url='https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=%s&count=200'
		request = urllib2.Request(url % user)
		request.add_header('Authorization', 'Bearer '+app.secret_key)
		request.add_header('User-Agent','AnalyzeUserTweet')
		while True:
			try:
				response = urllib2.urlopen(request)
				nextData = json.load(response)
			except urllib2.HTTPError, e:
	    			print e
				return e
			dateDifferenceOfLastRecord=_self.getDateDifference(nextData[len(nextData)-1][u'created_at'])
			dateDifferenceOfFirstRecord=_self.getDateDifference(nextData[0][u'created_at'])
			#if last record of list fits in span, then adding all records to collection
			if dateDifferenceOfLastRecord<=duration:
				data=data+nextData
			elif dateDifferenceOfFirstRecord>duration:
			#if first record doesnt fit in span, then dumping all records
				nextData=[]
			else:
				end=len(nextData)-1;
				start=0;
				mid=(start+end)/2
				#Using binary serach terminology, getting required records
				while True:
					dateDifference=_self.getDateDifference(nextData[mid][u'created_at'])
					if dateDifference>duration:
						del nextData[mid:end+1]
						dateDifference=_self.getDateDifference(nextData[mid-1][u'created_at'])
						end=mid-1
						mid=(start+end)/2
					else:
						start=mid+1
						mid=(start+end)/2
					if start>end:
						break
				data=data+nextData
			#if data left after removing unwanted records is less than count parameter,then breaking the loop to fetch more records
			if len(nextData)<200:
				break
			else:	
				url='https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=%s&count=200&max_id=%s'
				request = urllib2.Request(url % (user,(nextData[len(nextData)-1][u'id'])-1))
				request.add_header('Authorization', 'Bearer '+app.secret_key)
				request.add_header('User-Agent','AnalyzeUserTweet')
		data=_self.analyzeData(data,duration+1)
		return data

	#Function to days from current date
	def getDateDifference(_self,date):
		createdDate=date.encode('ascii','ignore')
		createdDate=createdDate.split(" ")
		createdDate=createdDate[1]+" "+createdDate[2]+" "+createdDate[5]
		createdDate=datetime.datetime.strptime(createdDate,"%b %d %Y")
		n_date = datetime.datetime.now()
		dateDifference = abs(n_date - createdDate)
		return dateDifference.days

	#Function to aggregate tweet count
	def analyzeData(_self,data,duration):
		divisor=1
		aggregatedTweets=[]
		"""If duration>10 then keeping count in block of (duration/10) days else for single day"""
		if duration>10:
			divisor=10
			aggregatedTweets=[0]*(duration/divisor)
		else:
			aggregatedTweets=[0]*duration
		for i in data:
			dateDifference=_self.getDateDifference(i[u'created_at'])
			dateDifference=dateDifference/divisor
			"""If duration>10 then adding extra days to last block
			   Example: if duration=64 then keeping count from 0-49 in 0-4 block and 50-63 in 5th block"""
			if dateDifference>=len(aggregatedTweets):
				dateDifference=len(aggregatedTweets)-1
			aggregatedTweets[dateDifference]+=1
			
		return aggregatedTweets

	#Function to generate final collection with respective time span of tweet count
	def generateJSON(_self,data1,data2,duration,user1,user2):
		divisor=1
		if duration>10:
			divisor=10
		n_date = datetime.datetime.now()
		tweetsData=[]
		#If duration>10 then adding range to time span
		if duration>10:
			for i in xrange(0,len(data1)-1):
				date = n_date - datetime.timedelta(days=i*divisor)
				tweetsPeriod = str(date.day) + "/" + str(date.month)
				date = n_date - datetime.timedelta(days=(i+1)*divisor-1)
				tweetsPeriod = tweetsPeriod + " - " + str(date.day) + "/" + str(date.month)
				temp={}
				temp['period']=tweetsPeriod
				temp[user1]=data1[i]
				temp[user2]=data2[i]
				tweetsData.append(temp)
			"""If duration>10 then adding extra days to last block
			   Example: if duration=64 then keeping count from 0-49 in 0-4 block and 50-63 in 5th block"""
			date = n_date - datetime.timedelta(days=(len(data1)-1)*divisor)
			tweetsPeriod = str(date.day) + "/" + str(date.month)
			date = n_date - datetime.timedelta(days=duration-1)
			tweetsPeriod = tweetsPeriod + " - " + str(date.day) + "/" + str(date.month)
			temp={}
			temp['period']=tweetsPeriod
			temp[user1]=data1[len(data1)-1]
			temp[user2]=data2[len(data2)-1]
			tweetsData.append(temp)
		else:
			for i in xrange(0,len(data1)):
				date = n_date - datetime.timedelta(days=i)
				tweetsPeriod = str(date.day) + "/" + str(date.month)
				temp={}
				temp['period']=tweetsPeriod
				temp[user1]=data1[i]
				temp[user2]=data2[i]
				tweetsData.append(temp)
		return tweetsData
			
