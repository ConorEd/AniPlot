######### Python Script to created animated or static plot ######### 
######### for cells in electrode.			   #########
## author: Conor Edwards					  ##
## date: 26.01.18						  ##
####################################################################

import getpass
import matplotlib.pyplot as plt
#import matplotlib as ax
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import numpy as np
import csv
from mpl_toolkits.mplot3d import Axes3D
from tkinter import Tk
from tkinter import filedialog
from textwrap import wrap

############    Script Options   ###############
duration = 60 					#Duration of imaging sequence in seconds.
interval = 0.5  				#Interval between image capture in seconds.
outputdir = "/output/" 			#Name for output file to be saved as.
animated = "T" 					# "T" = animated plot; "F" = static plot.
fps = 30					#Movie Frames per Second - ignore if animated != "T"
zap = "T" 					#True ("T") if cells were shocked to mark shock time.
shockframe = 10  				#Frame at which cells were shocked (in seconds)

#DEBUG
DEBUG = "F" 					#if true ("T") data will be printed and extra catches presented
#################################################
######  Console Queries  ######
title = input('Enter Figure Title: ')
xlab = input('Enter x-axis label: ')
ylab = input('Enter y-axis label: ')
savename = input('Enter name of output file: ')		#add error-catch for non Y/N 


######	.CSV Opening  ######
Tk().withdraw()
filename = filedialog.askopenfilename()
data = np.genfromtxt(filename, delimiter = ',', skip_header = 1, names = ['y'], dtype=['float'])
ntimepoints = ((duration/interval) + 1)
x = np.linspace(0, duration, num=ntimepoints) #for 60 second timelapse with 500ms interval
y = data['y']

if DEBUG == "T":
	print(x)
	print(y)	

######  Plotting Base  ######

fig, ax = plt.subplots()
maxX = (max(x))	
minX = (min(x))
maxY = (max(y)+5)
minY = (min(y)-5)
#plt.title(title)
ax.set_title("\n".join(wrap(title, 60)))
plt.xlabel(xlab)
plt.ylabel(ylab)
plt.grid(True)
xticks = [0, 10, 20, 30, 40, 50, 60]
plt.xticks(xticks)
if zap == "T":
	shocktime = shockframe*interval	
	plt.axvline(x = 5, color = 'black')   
	#ax.text(6, (maxY-2), 'i', style = 'italic', fontsize = 12)


######  Animated Plot  ######
if animated == "T":
	#maxX = (max(x))	
	#minX = (min(x))
	#maxY = (max(y)+10)
	#minY = (min(y)-10)	
	line, = ax.plot([], [], 'k-', color='r', lw = 6)	
	user = getpass.getuser()
	Writer = animation.writers['ffmpeg']
	writer = Writer(fps=fps, metadata=dict(artist=user), bitrate=1800)
	def init():
		line.set_data(x[:2], y[:2])
		plt.ylim((minY-10), (maxY+10))		
		plt.xlim(minX, maxX)	
		return line,
	def animate(i):
		#win = 300
		#imin = min(max(0, i - win), x.size - win)	
		#xdata = x[imin:i]
		#ydata = y[imin:i]
		i = min(i, x.size)			
		xdata = x[:i]
		ydata = y[:i]	
		ax.relim()
		#ax.autoscale(axis='x')	
		line.set_data(xdata, ydata)
		#ax.relim()
		#ax.autoscale(axis='x')
		return line,


	ani = FuncAnimation(
		fig, animate, frames=121, init_func=init, interval=15)
	
	#if save == "Y":
	saveout = savename + ".mp4"
	ani.save(saveout, writer=writer)
	
	plt.show()

######  Static Plot  ######
else:
	line = ax.plot(x, y, color='r', lw = 6)
	if save == "Y":
		saveout = outputdir + savename + ".png"
		fig.savefig(saveout)
	plt.show()	

