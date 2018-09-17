import os, sys, praw, json
import pprint as p


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
	for comment in morejpeg_auto.comments.new(limit=50):
		for checked_comment in checked_comments:
			if checked_comment["id"] == comment.id:
				# if this happens previous comments will already have been checked, so we can
				# exit without missing out on stuff
				print("\n\nStopping after %d, I already visited https://reddit.com%s" %
					(i, comment.permalink))
				exit(0)

		i += 1
		sys.stdout.write("\rChecking: #%d" % i)
		sys.stdout.flush()

		answered_by_us = False

		# something is broken with comment.replies if we don't do .refresh()
		# also .refresh() throws if the comment was deleted, so well need to catch that
		try:
			comment.refresh()

			for reply in comment.replies:
				for line in iter(reply.body.splitlines()):
					if "more" in line.lower() and "jpeg" in line.lower():
						# don't answer if the comment is pretty new, we want to 
						# give u/morejpeg some time (at least 30min)
						# TODO

						# check if it was answered by u/morejpeg_auto
						was_answered = False
						for replyreply in reply.replies:
							if (replyreply.author.name == "morejpeg_auto" or
								replyreply.author.name == "4x_jpeg"):
								
								was_answered = True
								break
						
						if not was_answered:
							if input("\nComment on https://reddit.com%s? [y/N]: "
								% reply.permalink).lower() == "y":

								reply.reply(
									">%s\n"
									"\n"
									"u/morejpeg_auto doesn't seem to answer you, so I'll help"
									" out:\n"
									"[Here you go!](%s)\n"
									"\n\n\n"
									"^^^I ^^^am ^^^a ^^^bot\n\n"
									"[GitHub](https://github.com/Nunu-Willump/4x_jpeg_bot.git)"
									% (
										line,

										# add number of checked comments to index
										# to have it not repeat after each run
										blackholed_urls[(i + len(checked_comments))
											% len(blackholed_urls)]
									)
								)
								answered_by_us = True
						
						# dont continue with this comment if the last line triggered the if
						continue

		# something is wrong with the comment, and that won't change as we already called
		# comment.refresh()
		except AttributeError:
			pass
		# this happens at comment.refresh() if the comment was deleted
		except praw.exceptions.ClientException:
			pass

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
