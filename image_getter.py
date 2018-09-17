import praw, json
import requests as r


reddit = praw.Reddit(
	client_id="0V1g_2X1ayVenw",
	client_secret=input("secret: "),
	user_agent="unix:4x_jpeg_bot:alpha (by /u/4x_jpeg)"
)

image_list = []

for submission in reddit.subreddit("blackholedmemes").new(limit=200):
	try:
		# submission.url not existing gets catched, http status error too
		img = r.get(submission.url, timeout=20, stream=True)
		img.raise_for_status()

		print("Downloading \"%s\" (%s)..." % (submission.title, submission.url))
		f = open("images/" + submission.url.split("/")[-1], "wb")
		f.write(img.content)
		image_list.append(submission.url)
	except AttributeError:
		pass
	except r.exceptions.HTTPError:
		pass
	except r.exceptions.Timeout:
		pass
	finally:
		f_json = open("image_list.json", "w")
		f_json.write(json.dumps(image_list, indent=4))
		f_json.close()