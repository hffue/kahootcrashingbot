import praw
import config

def init():
	try:
		DB = open("processed.txt", "r")
		DB.close()
	except:
		DB = open("processed.txt", "w+")
		DB.close()

def main():
	print ('Logging in')
	reddit = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = config.user_agent)
	
	subreddit = reddit.subreddit(config.target_subreddit)		
	for submission in subreddit.stream.submissions():
		if stringsplit(submission.title) and submissioncheck(submission):
			savesubmission(submission)
			runbot(submission)

def runbot(submission):
	print(submission.title)
	print('Replying to: ',submission.title)
	submission.reply(submission.title)

def stringsplit(submission):
	return True

def submissioncheck(submission):
	DB = open("processed.txt", "r")
	IDs = DB.read()
	if submission.id in IDs:
		DB.close()
		return False

	DB.close()
	return True

def savesubmission(submission):
	DB = open("processed.txt", "a")
	DB.write('[' + submission.id + ' , "' + submission.title + '"] - ')
	print('Saved submission "', submission.title, '"')

init()

if __name__ == '__main__':
	main()
