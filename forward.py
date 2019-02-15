import praw
import config

def init():
	try:
		msgDB = open("forwarded.txt", "r")
		msgDB.close()
	except:
		msgDB = open("forwarded.txt", "w+")
		msgDB.close()

def main():
	print ('Loading forwarding bot\n')
	reddit = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = config.user_agent)
	
	for message in reddit.inbox.stream():
		if messagecheck(message):
			print("Forwarding message: ")
			print("Subject: " + message.subject)
			print("Body: " + message.body)
			print("Sent by: u/" + str(message.author))
			savemessage(message)
			subject = message.subject
			body = ("Message: " + message.body + "\n \n From u/" + str(message.author))
			reddit.redditor('PMMEURTHROWAWAYS').message(subject, body)

def messagecheck(message):
	msgDB = open("forwarded.txt", "r")
	msgIDs = msgDB.read()
	if message.id in msgIDs:
		msgDB.close()
		return False

	msgDB.close()
	return True

def savemessage(message):
	try:
		msgDB = open("forwarded.txt", "a")
		msgDB.write('[' + message.id + ' , "' + message.subject + '"] - ')
		msgDB.close()
	except:
		msgDB = open("forwarded.txt", "a")
		msgDB.write('[' + message.id + ' , ERROR: Could not display part of message] - ')
		msgDB.close()

init()

if __name__ == '__main__':
	main()
