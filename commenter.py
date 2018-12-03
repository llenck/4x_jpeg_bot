import os, sys, praw, json, datetime
import pprint as p


banned_subs = (
	"SuicideWatch",
	"depression",
	"test", # would comment without being asked to because it replies to u/MarkdownShadowBot
	"discordapp", # those fuckers banned me so no need to waste cpu time here
)

if not os.path.isfile("checked_comments.json"):
	checked_comments = []
else:
	with open("checked_comments.json", "r") as f:
		checked_comments = json.loads(f.read())

with open("image_list.json", "r") as f:
	blackholed_urls = json.loads(f.read())

# allow client secret and password to be set manually or by environment for automating
try:
	secret = os.environ["CLIENT_SECRET"]
except KeyError:
	secret = input("secret: ")

try:
	pw = os.environ["REDDIT_PASSWORD"]
except KeyError:
	pw = input("password: ")

reddit = praw.Reddit(
	client_id="0V1g_2X1ayVenw",
	client_secret=secret,
	user_agent="unix:4x_jpeg_bot:alpha (by /u/4x_jpeg)",
	username="4x_jpeg",
	password=pw
)

morejpeg_auto = reddit.redditor("morejpeg_auto")

try:
	i = 0
	for comment in morejpeg_auto.comments.new(limit=10):
		i += 1
		sys.stdout.write("\rChecking: #%d (%s)" % (i, comment.permalink))
		sys.stdout.flush()

		# no need to check already checked comments
		skip = False
		for checked_comment in checked_comments:
			if checked_comment["id"] == comment.id:
				skip = True
				break
		if skip:
			continue

		for sub in banned_subs:
			if comment.subreddit.display_name == sub:
				skip = True
				break
		if skip:
			continue

		# if this comment is new and stuff might change, we need a way to tell 
		# later parts of the code to not record this
		too_early_to_skip = False

		# don't skip next run if u/morejpeg_auto's comment is less than 10h old
		if int(datetime.datetime.utcnow().timestamp()) < comment.created_utc + 36000:
			too_early_to_skip = True


		# for the record, out of curiosity (lul)
		answered_by_us = False

		# something is broken with comment.replies if we don't do .refresh()
		# also .refresh() throws if the comment was deleted, so well need to catch that
		try:
			comment.refresh()

			for reply in comment.replies:
				# don't answer if the comment is pretty new, we want to
				# give u/morejpeg some time (at least 10min)
				if int(datetime.datetime.utcnow().timestamp()) < reply.created_utc + 600:
					too_early_to_skip = True
					continue
				
				for line in iter(reply.body.splitlines()):
					# if someone writes "morejpeg" they probably are just talking about
					# the bot and not actually requesting more jpeg
					if (("more" in line.lower() and "jpeg" in line.lower())
						or ("needs" in line.lower() and "jpeg" in line.lower())
						) and not "morejpeg" in line.lower():

						# check if it was answered by u/morejpeg_auto
						was_answered = False
						for replyreply in reply.replies:
							if (replyreply.author.name == "morejpeg_auto" or
								replyreply.author.name == "4x_jpeg"):
								
								was_answered = True
								break
						
						if not was_answered:
							reply.reply(
								">%s\n"
								"\n"
								"u/morejpeg_auto doesn't seem to answer you,"
								" so I'll help out:\n"
								"[Here you go!](%s)\n"
								"\n"
								"\n"
								"^^^(I am a bot and I don't answer to replies, though my master might.)\n"
								"\n"
								"While you're on the internet, please sub to PewDiePie und unsub from T-Series. It's a close battle by now :/\n"
								"\n"
								"[GitHub]"
								"(https://github.com/Nunu-Willump/4x_jpeg_bot.git)\n"
								""
								% (
									line,

									# add number of checked comments to index
									# to have it not repeat after each run
									blackholed_urls[(i + len(checked_comments))
										% len(blackholed_urls)]
								)
							)
							answered_by_us = True
							too_early_to_skip = False

						# dont continue with this reply if the last line triggered the if
						continue

		# something is wrong with the comment, and that won't change as we already called
		# comment.refresh()
		except AttributeError:
			pass
		# this happens at comment.refresh() if the comment was deleted
		except praw.exceptions.ClientException:
			pass

		if not too_early_to_skip:
			checked_comments.append({"id": comment.id,
				"body": comment.body, "link": "https://reddit.com" + comment.permalink,
				"Answered": answered_by_us})

except Exception as e:
	sys.stdout.write("\n\nCaught %s." % repr(e))
# also catch keyboard interrups and other shit so the json file always gets updated
except:
	sys.stdout.write("\n\nCaught something. Idk though.")

print("\n\nGimme a sec to update the json file...")
f = open("checked_comments.json", "w")
f.write(json.dumps(checked_comments, indent=4))
f.close()
exit(0)
