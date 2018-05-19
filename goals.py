import matplotlib
matplotlib.use("Agg")
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import matplotlib.pyplot as plt
import numpy as np
import requests
import json
import sphviewer as sph

x=[]
y=[]
z=[]

#The starting year of the season (by default this is the 2017-2018 season).
#The earliest year that will work is 2010.
YEAR = "2017"

#Constants for the type of games played
PRESEASON = "01"
REGULARSEASON = "02"
PLAYOFFS = "03"
ALLSTAR = "04"

#This function was taken from StackOverflow user Alejandro here:
#https://stackoverflow.com/a/36515364
def myplot(x, y, nb=32, xsize=500, ysize=500):   
    xmin = np.min(x)
    xmax = np.max(x)
    ymin = np.min(y)
    ymax = np.max(y)

    x0 = (xmin+xmax)/2.
    y0 = (ymin+ymax)/2.

    pos = np.zeros([3, len(x)])
    pos[0,:] = x
    pos[1,:] = y
    w = np.ones(len(x))

    P = sph.Particles(pos, w, nb=nb)
    S = sph.Scene(P)
    S.update_camera(r='infinity', x=x0, y=y0, z=0, 
                    xsize=xsize, ysize=ysize)
    R = sph.Render(S)
    R.set_logscale()
    img = R.get_image()
    extent = R.get_extent()
    for i, j in zip(xrange(4), [x0,x0,y0,y0]):
        extent[i] += j
    return img, extent

#Loop through every game in a season (1271 for 31 teams)
for i in range(1,1272):
   try:
      #Get the API url
      url = "https://statsapi.web.nhl.com/api/v1/game/" + YEAR + REGULARSEASON + str("%04d" %(i,)) + "/feed/live"
      response = requests.get(url)
      for j in range(1000):
         try:
            if response.json()["liveData"]["plays"]["allPlays"][j]["result"]["event"] == "Goal":
               #If a goal was scored, append the x and y coordinates to their respective lists
               x.append(float(response.json()["liveData"]["plays"]["allPlays"][j]["coordinates"]["x"]))
               y.append(float(response.json()["liveData"]["plays"]["allPlays"][j]["coordinates"]["y"]))

               #Create a figure with four subplots. One for the scatter plot, and the others are heatmaps
               fig = plt.figure(1, figsize=(35,15))
               fig.suptitle("Goals in game " + str(i),fontsize=30,y=1.0004)
               ax1 = fig.add_subplot(221)
               ax2 = fig.add_subplot(222)
               ax3 = fig.add_subplot(223)
               ax4 = fig.add_subplot(224)
               ax1.tick_params(labelsize=20)
               ax2.tick_params(labelsize=20)
               ax3.tick_params(labelsize=20)
               ax4.tick_params(labelsize=20)
               img = plt.imread("rink.png")	#Set the background of the scatter plot to an ice rink
               ax1.imshow(img,extent=[-100,100,-42.5,42.5])
	       ax1.plot(x,y,'k.', markersize=10)
               ax1.set_title("Coordinate Scatter Plot",fontsize=30)
               ax1.set_xlim(-100,100)
               ax1.set_ylim(-42.5,42.5)

	       #Create the heat maps
               heatmap_16,extent_16 = myplot(x,y, nb=16)
               heatmap_32,extent_32 = myplot(x,y, nb=32)
               heatmap_64,extent_64 = myplot(x,y, nb=64)
               ax2.imshow(heatmap_16, extent=[-100,100,-42.5,42.5], origin='lower', interpolation = "none", vmin = 0,aspect='auto')
               ax2.set_title("Heatmap (smoothing over 16 goals)",fontsize=30)
               ax2.set_xlim(-100,100)
               ax2.set_ylim(-42.5,42.5)
               ax3.imshow(heatmap_32, extent=[-100,100,-42.5,42.5], origin='lower', aspect='auto')
               ax3.set_title("Heatmap (smoothing over 32 goals)",fontsize=30)
               ax3.set_xlim(-100,100)
               ax3.set_ylim(-42.5,42.5)
               ax4.imshow(heatmap_64, extent=[-100,100,-42.5,42.5], origin='lower', aspect='auto')
               ax4.set_title("Heatmap (smoothing over 64 goals)",fontsize=30)
               ax4.set_xlim(-100,100)
               ax4.set_ylim(-42.5,42.5)

	       #Save the image in the images/ directory and clear the figure for the next game
               plt.savefig("images/GoalLocation"+str(i)+".png")
               plt.clf()

         except IndexError:
            break
   except KeyError:
      continue
