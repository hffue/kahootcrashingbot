import praw
import config

def bot_login():
	print "Logging in..."
	reddit = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = config.user_agent)
			
	return reddit
	

def run_bot(reddit):
	subreddit = reddit.subreddit(config.target_subreddit)
	for submission in subreddit.stream.submissions()
			print "I have no idea what to do here so far..."


