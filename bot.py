import praw
import subprocess
import os
import config

total = 0

def init():
	try:
		DB = open("processed.txt", "r")
		DB.close()
	except:
		DB = open("processed.txt", "w+")
		DB.close()

def main():
	forward = subprocess.Popen("python forward.py")
	print (forward)
	print ('Loading main bot\n')
	reddit = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = config.user_agent)
	
	subreddit = reddit.subreddit(config.target_subreddit)		
	for submission in subreddit.stream.submissions():
		proctitle = processtitle(submission)
		if proctitle and submissioncheck(submission):
			if config.save:
				savesubmission(submission)
			checkamt(submission, proctitle)	

		if proctitle and not submissioncheck(submission):
			print('Post [',submission.title,'] has already been processed\n\n','--------------------------------------------------------------------------------\n')
		
		if not proctitle and submissioncheck(submission):
			if config.save:
				savesubmission(submission)
			print('Post [',submission.title,'] was too short, ignoring post\n\n','--------------------------------------------------------------------------------\n')
		
		if not proctitle and not submissioncheck(submission):
			print('Post [',submission.title,'] was both too short and already processed\n\n','--------------------------------------------------------------------------------\n')

def checkamt(submission, proctitle):
	amount = int(proctitle[1],10)
	if amount < 1001:
		runbot1(submission, proctitle)
	if amount >= 1001:
		runbot2(submission, proctitle)

def runbot1(submission, proctitle):
	reply = ('###Attempting to flood game *' + proctitle[0] + '* with *' + proctitle[1] + '* bots named *' + proctitle[2] + '*\n \n##^(Games botted: ' + str(total) + ') \n ___ \n \n ^(I am a bot, this action was performed automatically.) \n \n^(If you have any questions please PM me, and I will forward your message to my developer.) \n \n^(All of my code is visible here: https://github.com/cymug/kahootcrashingbot)\n \n^v. ^0.1.0')
	if config.comments:
		submission.reply(reply)
	print('Replied to:',submission.title,'\n')
	command = (r'go run main.go ' + proctitle[0] + ' "' + proctitle[2] + '" ' + proctitle[1])
	if config.join:
		bot = subprocess.Popen(command)
		print(bot)
	print('Successfully ran bot on game [', submission.title, ']\n\n','--------------------------------------------------------------------------------\n')
	return True

def runbot2(submission, proctitle):
	reply = ('###Attempting to flood game *' + proctitle[0] + '* with *1000* bots named *' + proctitle[2] + '* \n \n ^(Bot limit is currently set to 1000)\n \n##^(Games botted: ' + str(total) + ') \n ___\n \n ^(I am a bot, this action was performed automatically.) \n \n^(If you have any questions please PM me, and I will forward your message to my developer.) \n \n^(All of my code is visible here: https://github.com/cymug/kahootcrashingbot)\n \n^v. ^0.1.0')
	if config.comments:
		submission.reply(reply)
	print('Replied to:',submission.title,'\n')
	limit = str(1000)
	command = (r'go run main.go ' + proctitle[0] + ' "' + proctitle[2] + '" ' + limit)
	if config.join:
		bot = subprocess.Popen(command)
		print(bot)
	print('Successfully ran bot on game [', submission.title, ']\n\n','--------------------------------------------------------------------------------\n')
	return True

def converttitle(proctitle):
	try:
		proctitle[0] = int(proctitle[0],10)
		proctitle[1] = int(proctitle[1],10)
		return proctitle
	except:
		return proctitle

def submissioncheck(submission):
	global total
	DB = open("processed.txt", "r")
	IDs = DB.read()
	if submission.id in IDs:
		DB.close()
		return False
	DB.close()
	total = len(IDs.split("] - ["))
	return True

def savesubmission(submission):
	try:
		DB = open("processed.txt", "a")
		DB.write('[' + submission.id + ' , "' + submission.title + '"] - ')
		print('Saved submission [', submission.title, ']\n')
		DB.close()
	except:
		DB = open("processed.txt", "a")
		DB.write('[' + submission.id + ' , ERROR: Could not parse title] - ')
		print('Saved submission [', submission.id, '] with title parse error\n')
		DB.close()

def processtitle(submission):
	processedtitle = submission.title.split(" | ", 4)
	shorttitle = processedtitle[:3]
	if len(shorttitle) == 3:
		return processedtitle
	else:
		return False

init()

if __name__ == '__main__':
	main()
