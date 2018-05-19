This project is used to create an animation showing the goals and heatmaps
for all goals scored in every NHL game in a given season (2017-2018 in my
case). Created by Justin Tomlinson.

To use, start by using:

	python goals.py

You will need matplotlib, numpy, requests, json, sphviewer and a few hours,
because this will likely take a long time to make all of the requests and
generate all of the plots.

Next you will want to use:

	python gifcreator.py

You will need imageio. If the pictures are not in the directory ./images/
then this will not work. The final gif will be in your current directory
called goals.gif and will likely be very large. If you don't want all of
those image files taking up space on your computer, simply use:

	source clearimages.sh

This will delete all image files in the ./image directory.
