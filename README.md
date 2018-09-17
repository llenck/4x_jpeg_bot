4x_jpeg_bot - For those who think 3x jpeg isn't enough
========

We all know u/morejpeg_auto.
But he stops after 3 times jpegging in a row. That sucks.
So I created a bot that finds cases where
u/morejpeg_auto didn't respond after a certain amount of time and answers people. Since jpegging a 4th time isn't going to do all that much (and I wanted it to be a little more extreme) it posts a random picture out of a list from r/blackholedmemes.

Project Structure
--------

All the work is actually done in commenter.py. The file isn't all that long so I won't explain the contents here. Though, I admit that I commited "Hold my beer I can do this all in main"

checked_comments.json (created after first run) stores information on comments already checked, and while it doesn't need to store all that information just to not double comment or check, just out of curiosity I did it in this verbose way.

image_list.json contains a list of links to usable images from r/blackholedmemes. Sometimes, the people over there post stuff that isn't completely blackholed, so I downloaded 200 images from there, filtered the bad ones out and put the rest into this list.

image_getter.py was used to download these images, so if you ever feel like downloading a ton of modern art, I left this file for you :p
