from itertools import cycle
from ggplot import *
import pandas as pd
import numpy 
from scipy import stats
import scipy as sp
import scipy.optimize

from matplotlib import style
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn as sns

###########################
#Settings for Graphs and Legends
left  = 0.175  # the left side of the subplots of the figure
right = 0.9    # the right side of the subplots of the figure
bottom = 0.18   # the bottom of the subplots of the figure
top = 0.57      # the top of the subplots of the figure
wspace = 0.35   # the amount of width reserved for blank space between subplots
hspace = 0.75   # the amount of height reserved for white space between subplots
width = 0.35		# Width of the tick marks and bars on each historgram
###########################
# '''
# Exponential Decay Function
# '''
# def DecayFunction(time,A,B,startTime,GAsymptote):
# 	GStart = A + GAsymptote
# 	return A * ( numpy.exp( -1*(time - startTime)/(B) ) ) + GAsymptote
# '''
# Inverse Exponential Decay Function
# '''
# def InverseDecayFunction(time,A,B,startTime,GStart):
# 	GAsymptote = A + GStart
# 	return A * ( 1 - numpy.exp( ( -1*(time - startTime)/(B) ) ) ) + GStart
'''
Exponential Decay Function
'''
def DecayFunction(time,Tau,GStart,GAsymptote):
	return (GStart - GAsymptote) * (numpy.exp( -1*time/(Tau) )) + GAsymptote
'''
Inverse Exponential Decay Function
'''
def InverseDecayFunction(time,Tau,GStart,GAsymptote):
	return (GAsymptote - GStart) * ( 1 - numpy.exp( ( -1*time/(Tau) ) ) ) + GStart

# style.use('bmh')
style.use('ggplot')

def summarizeStatistics(data_Matrix):
	transpose = zip(*data_Matrix) 
	
	x_axis = []
	for i in range(0, len(transpose[0]) ):
		x_axis.append(i + 1)
	fileNamesOnly = []
	
	for string in transpose[0]:
		fileNamesOnly.append( string.split("/")[1] )
	
	#Open the pdf
	with PdfPages('SummaryGraphs.pdf') as pdf:

		###########################
		#Create a box plot for summary statistics 
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.set_ylabel('Conduction',color='black', fontsize=14)
		ax.set_xlabel('Genotype',color='black', fontsize=14)
		ax.tick_params(labelsize=14)
		plt.title('Box Plots of Conductance',y=1.08,fontsize=16)
		fig.set_size_inches(14.5, 10.5)

		#Create Box Plot using conductance
		ax.boxplot(transpose[12])
		#Use the plantids
		xtickNames = ax.set_xticklabels(fileNamesOnly)
		plt.setp(xtickNames, rotation=75, fontsize=12)
		
		plt.tight_layout()
		pdf.savefig()
		plt.close()
		
		###########################

		#Create a bar plot of the constant baseline conductance
		fig = plt.figure()
		ax = fig.add_subplot(111)
		fig.set_size_inches(14.5, 10.5)
		ax.tick_params(labelsize=12)
		bars = []
		colors = cycle(["aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal", "yellow"])
		
		#create first bar graph of the baselines
		for i in range ( len(x_axis) ):
			rects = ax.bar(x_axis[i], transpose[13][i][0], 0.35, color=next(colors))
			bars.append( rects )

		#Set the range of x and add tick marks and tick labels
		ax.set_xlim(-width,len(x_axis) + 1 + width)
		ax.set_xticks(x_axis)
		xtickNames = ax.set_xticklabels(transpose[4])
		plt.setp(xtickNames, rotation=45, fontsize=14)
		
		# Name the y and x axis, and title
		ax.set_ylabel('Conduction',color='black',fontsize=14)
		ax.set_xlabel('Genotype',color='black',fontsize=14)
		plt.title('Mode of BLCond Column',y=1.08,fontsize=16)
		
		#Create the legend for image and add to new pdf page
		plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
		plt.legend((bars),(transpose[0]),bbox_to_anchor=((0., 1.82, 1., .182)), loc=1, ncol=3, mode="expand", borderaxespad=0.,prop={'size':12},title="Files and Their Folder Name Plotted Below")
		pdf.savefig()
		plt.close()
		
		###########################
		
		#Create a bar plot of the slope of the baseline conductance
		fig = plt.figure()
		ax = fig.add_subplot(111)
		fig.set_size_inches(14.5, 10.5)
		ax.tick_params(labelsize=12)
		bars1 = []
		colors = cycle(["aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal", "yellow"])
		
		means = []

		#Create bar graph in slopes
		for i in range ( len(x_axis) ):
			x, y = numpy.array(transpose[14][i][0],dtype=numpy.float64), numpy.array(transpose[15][i][0],dtype=numpy.float64)
			slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
			means.append(numpy.mean(y))
			rects = ax.bar(x_axis[i], slope, 0.35, color=next(colors))
			bars1.append( rects )
		
		#Set the range of x and add tick marks and tick labels
		ax.set_xlim(-width,len(x_axis) + 1 + width)
		ax.set_xticks(x_axis)
		xtickNames = ax.set_xticklabels(transpose[4])
		plt.setp(xtickNames, rotation=45, fontsize=14)
		ax.set_ylabel('Conduction',color='black', fontsize=14)
		ax.set_xlabel('Genotype',color='black', fontsize=14)
		plt.title('Slope of Baseline Conductance',y=1.08,fontsize=16)
		plt.axhline(0, color='black')
		plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
		plt.legend((bars1),(transpose[0]),bbox_to_anchor=((0., 1.82, 1., .182)), loc=1, ncol=3, mode="expand", borderaxespad=0.,prop={'size':12},title="Files and Their Folder Name Plotted Below")
		pdf.savefig()
		plt.close()

		###########################
		
		#Create a bar plot of the slope of the baseline conductance
		fig = plt.figure()
		ax = fig.add_subplot(111)
		fig.set_size_inches(14.5, 10.5)
		ax.tick_params(labelsize=12)
		bars1 = []
		colors = cycle(["aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal", "yellow"])
		
		#Create bar graph in slopes
		for i in range ( len(x_axis) ):
			rects = ax.bar(x_axis[i], means[i], 0.35, color=next(colors))
			bars1.append( rects )
		
		#Set the range of x and add tick marks and tick labels
		ax.set_xlim(-width,len(x_axis) + 1 + width)
		ax.set_xticks(x_axis)
		xtickNames = ax.set_xticklabels(transpose[4])
		plt.setp(xtickNames, rotation=45, fontsize=14)
		ax.set_ylabel('Conduction',color='black', fontsize=14)
		ax.set_xlabel('Genotype',color='black', fontsize=14)
		plt.title('Mean of Baseline Conductance',y=1.08,fontsize=16)
		plt.axhline(0, color='black')
		plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
		plt.legend((bars1),(transpose[0]),bbox_to_anchor=((0., 1.82, 1., .182)), loc=1, ncol=3, mode="expand", borderaxespad=0.,prop={'size':12},title="Files and Their Folder Name Plotted Below")
		pdf.savefig()
		plt.close()

		###########################
		#Create Max and Min Side by Side Bar Graphs for Each CO2 Setting Separately
	
		#Count the unique CO2 settings
		distinctSettingsC02 = set()
		for CO2_set in transpose[5]:
			for level in CO2_set:
				if level not in distinctSettingsC02:
					distinctSettingsC02.add(int(level))

		#Create a graph for each distinct level
		for distinct_level in distinctSettingsC02:
			#Extract the following from each paramter
			x_axis, maxG, minG, onlyFileName, fittingParameters = [], [] , [] , [], []
			#For each possible file, check if it has the current distinct CO2 setting

			for i in range( 0, len(transpose[5]) ):
				#If it does have the CO2 setting to make a graph for: add all necessary data
	
				if int(distinct_level) in map(int,transpose[5][i]):
					x_axis.append(i + 1)
					CO2_level_index = transpose[5][i].index(distinct_level)
					maxG.append(max(transpose[15][i][CO2_level_index]))
					minG.append(min(transpose[15][i][CO2_level_index]))
					onlyFileName.append(transpose[0][i].split("/")[1])	
					
					#Run a non linear fit on the current portion of data
					opt_parms = []
					parm_cov = [[]]
					Tau, A, K, GAsymptote, GStart = 0, 0, 0, 0, 0

					#Get the time and scale it back down to 0
					time_raw = transpose[14][i][CO2_level_index]
					startTime = min(time_raw)
					linearize = lambda x: x-startTime
					time = map(linearize,time_raw)

					#Init conditions for exponential fitting
					cond = transpose[15][i][CO2_level_index]
					Tau, GAsymptote, GStart = 1, 1, 1
					opt_parms, parm_cov = [], [[]]
	
					#Inverse Exponential
					if (int(distinct_level) == 400) or (int(distinct_level) == 150):
						#Guess
						Tau, GAsymptote, GStart = 300, max(cond), min(cond)
						opt_parms, parm_cov = sp.optimize.curve_fit(InverseDecayFunction, time, cond,p0=( Tau, GStart, GAsymptote ),maxfev=500000)
						# print distinct_level , " Start: " + str(GStart), " End: " + str (GAsymptote), " Tau: " + str(numpy.log(Tau)), transpose[4][i]
					#Exponential Decay
					else:
						#Guess
						Tau, GAsymptote, GStart = 500, min(cond), max(cond)
						opt_parms, parm_cov = sp.optimize.curve_fit(DecayFunction,time, cond,p0=( Tau, GStart, GAsymptote ),maxfev=500000)	
					
					
					Tau, GStart, GAsymptote = opt_parms[0], opt_parms[1], opt_parms[2]
					Tau = numpy.log(Tau)
					# print distinct_level , " Start: " + str(GStart), " End: " + str (GAsymptote), " Tau: " + str(numpy.log(Tau)), transpose[4][i]
					if Tau < 0 or Tau > 20:
						Tau = 0 
					if GStart < 0 or GStart > 10:
						GStart = 0
					if GAsymptote < 0 or GAsymptote > 10:
						GAsymptote = 0
					fittingParameters.append([Tau, GStart, GAsymptote])
						
			#Create Side by Side Plot for Min and Max values for Each CO2 Setting
			fig = plt.figure()
			ax = fig.add_subplot(111)
			fig.set_size_inches(14.5, 10.5)
			ax.tick_params(labelsize=12)
			colors = cycle(["blue",  "maroon"])
			for i in range ( len(x_axis) ):
				rects = ax.bar(x_axis[i], minG[i], 0.35, color=next(colors))
				rects1 = ax.bar(x_axis[i]+width, maxG[i], 0.35, color=next(colors))

			#Set the range of x and add tick marks and tick labels
			ax.set_xticks(x_axis)
			xtickNames = ax.set_xticklabels(onlyFileName)
			plt.setp(xtickNames, rotation=75, fontsize=14)
			ax.set_ylabel('Conductance',color='black',fontsize=14)
			ax.set_xlabel('File',color='black',fontsize=14)
			plt.title('Min and Max Conductance for ' + str(distinct_level) + "ppm",fontsize=16)

			#Make the legend
			blue_patch = mpatches.Patch(color='blue', label='Min Conductance')
			maroon_patch = mpatches.Patch(color='maroon', label='Max Conductance')
			plt.legend(handles=[blue_patch,maroon_patch])	

			#Format and Save
			plt.tight_layout()
			pdf.savefig()
			plt.close()

			#Create Side by Side Plot for Gstart and GAsymptote values for Each CO2 Setting
			fig = plt.figure()
			ax = fig.add_subplot(111)
			fig.set_size_inches(14.5, 10.5)
			ax.tick_params(labelsize=12)
			colors = cycle(["red",  "black"])
			for i in range ( len(x_axis) ):
				rects = ax.bar(x_axis[i], fittingParameters[i][1], 0.35, color=next(colors))
				rects1 = ax.bar(x_axis[i]+width, fittingParameters[i][2], 0.35, color=next(colors))

			#Set the range of x and add tick marks and tick labels
			ax.set_xticks(x_axis)
			xtickNames = ax.set_xticklabels(onlyFileName)
			plt.setp(xtickNames, rotation=75, fontsize=14)
			ax.set_ylabel('Conductance',color='black',fontsize=14)
			ax.set_xlabel('File',color='black',fontsize=14)
			plt.title('Starting Values and Asymptote ' + str(distinct_level) + "ppm",fontsize=16)

			#Make the legend
			red_patch = mpatches.Patch(color='red', label='Starting Value')
			black_patch = mpatches.Patch(color='black', label='Asymptote')
			plt.legend(handles=[red_patch,black_patch])	

			#Format and Save
			plt.tight_layout()
			pdf.savefig()
			plt.close()

			#Create Bar plot for Tau values for Each CO2 Setting
			fig = plt.figure()
			ax = fig.add_subplot(111)
			fig.set_size_inches(14.5, 10.5)
			ax.tick_params(labelsize=12)
			bars1 = []
			colors = cycle(["aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal", "yellow"])
			
			#Create bar graph of Taus
			for i in range ( len(x_axis) ):
				rects = ax.bar(x_axis[i], fittingParameters[i][0], 0.35, color=next(colors))
				bars1.append( rects )
			
			#Set the range of x and add tick marks and tick labels
			ax.set_xlim(-width,len(x_axis) + 1 + width)
			ax.set_xticks(x_axis)
			xtickNames = ax.set_xticklabels(transpose[4])
			plt.setp(xtickNames, rotation=45, fontsize=14)
			ax.set_ylabel('Tau, log(minutes) ',color='black', fontsize=14)
			ax.set_xlabel('Genotype',color='black', fontsize=14)
			plt.title('Taus for: ' + str(distinct_level) + "ppm",y=1.08,fontsize=16)
			plt.axhline(0, color='black')
			plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
			plt.legend((bars1),(transpose[0]),bbox_to_anchor=((0., 1.82, 1., .182)), loc=1, ncol=3, mode="expand", borderaxespad=0.,prop={'size':12},title="Files and Their Folder Name Plotted Below",fontsize=16)
			pdf.savefig()
			plt.close()

def loess(data_Matrix,legend_headings):
	# Get the data for each array
	plantids, Time, Cond, ci, H2O, CO2 = [],[],[],[],[],[]
	for data in data_Matrix:
		plantids.append(data[4])
		Time.append(data[9])
		Cond.append(data[12])
		ci.append(data[10])
		H2O.append(data[11])
		CO2.append(data[3])
	fileNamesOnly = []
	for string in legend_headings:
		fileNamesOnly.append( string.split(" : ")[1] )

	with PdfPages('ScatterPlots.pdf') as pdf:
		
		'''
		Get all plots Time vs (cond, ci, CO2, H2O) all on one page. 
		Add legend to each graph, add title to each graph
		'''
		for i in range(len(plantids)):
			fig = plt.figure()
			fig.set_size_inches(14.5, 18.5)
			ax = fig.add_subplot(211)

			np_Time = numpy.array(Time[i],dtype=numpy.float64)
			np_Cond = numpy.array(Cond[i],dtype=numpy.float64)
			df = pd.DataFrame({'Time (sec)':np_Time, 'Conduction':np_Cond})
			

			#Create the plot with scatter plot smooth function placed over the data
			ax = sns.regplot(x='Time (sec)', y="Conduction", data=df,lowess=True,ci=95, scatter_kws={"color":"black"},line_kws={"color":"blue"},marker="o")
			
			#Formating title and legend
			plt.title( "Time vs. Conduction",fontsize=16)

			blue_patch = mpatches.Patch(color='black', label= fileNamesOnly[i] + " data")
			maroon_patch = mpatches.Patch(color='blue', label='Goodness of fit line')
			plt.legend(handles=[blue_patch,maroon_patch])	

			#Add the second plot which is histogram
			ax1 = fig.add_subplot(212)
			
			ax1.tick_params(labelsize=14)
			ax1.hist(map(float,Cond[i]), 50, normed=1, facecolor='green', alpha=0.75)
			ax1.set_ylabel('Conductance Frequency',color='black',fontsize=14)
			ax1.set_xlabel('conductance Value',color='black',fontsize=14)
			plt.title('Histogram of Conductance Values',fontsize=16)
			
			#Make the legend for file title
			blue_patch = mpatches.Patch(color='green', label=fileNamesOnly[i])
			plt.legend(handles=[blue_patch])	
			plt.tight_layout()
			pdf.savefig()
			plt.close()

# def histogram(plotTable,folder_files, legend_headings):

# 	fileNamesOnly = []
# 	for string in legend_headings:
# 		fileNamesOnly.append( string.split(" : ")[1] )

# 	#Initalize empty arrays
# 	baselines, plantids, slopes, x_axis, Taus, CriticalPoints, conductance = [], [], [], [], [], [], []

# 	#Extract data from plotTable and palce in appropriate arrays
# 	for index in range ( len(plotTable) ):
# 		plantids.append(plotTable[index][0])
# 		baselines.append(plotTable[index][1])
# 		slopes.append(plotTable[index][2])
# 		x_axis.append(index+1)
# 		Taus.append(plotTable[index][4])
# 		CriticalPoints.append(plotTable[index][5])
# 		conductance.append(plotTable[index][6])



	
# 	with PdfPages('SummaryGraphs.pdf') as pdf:

# 		###########################
# 		#Create a box plot for summary statistics 
# 		fig = plt.figure()
# 		ax = fig.add_subplot(111)
# 		ax.set_ylabel('Conduction',color='black', fontsize=14)
# 		ax.set_xlabel('File Names',color='black', fontsize=14)
# 		ax.tick_params(labelsize=14)
# 		plt.title('Box Plots of Conductance',y=1.08,fontsize=16)
# 		fig.set_size_inches(14.5, 10.5)

# 		#Create Box Plot
# 		ax.boxplot(conductance)

# 		xtickNames = ax.set_xticklabels(fileNamesOnly)
# 		plt.setp(xtickNames, rotation=75, fontsize=12)
		
# 		plt.tight_layout()
# 		pdf.savefig()
# 		plt.close()
# 		###########################

# 		#Create a bar plot of the mean of the baseline conductance
# 		fig = plt.figure()
# 		ax = fig.add_subplot(111)
# 		fig.set_size_inches(14.5, 10.5)
# 		ax.tick_params(labelsize=12)
# 		bars = []
# 		colors = cycle(["aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal", "yellow"])
		
# 		#create first bar graph of the baselines
# 		for i in range ( len(x_axis) ):
# 			rects = ax.bar(x_axis[i], baselines[i], 0.35, color=next(colors))
# 			bars.append( rects )

# 		#Set the range of x and add tick marks and tick labels
# 		ax.set_xlim(-width,len(x_axis) + 1 + width)
# 		ax.set_xticks(x_axis)
# 		xtickNames = ax.set_xticklabels(plantids)
# 		plt.setp(xtickNames, rotation=45, fontsize=14)
		
# 		# Name the y and x axis, and title
# 		ax.set_ylabel('Conduction',color='black',fontsize=14)
# 		ax.set_xlabel('Plantid',color='black',fontsize=14)
# 		plt.title('Mean of Baseline Conductance',y=1.08,fontsize=16)
		
# 		#Create the legend for image and add to new pdf page
# 		plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
# 		plt.legend((bars),(legend_headings),bbox_to_anchor=((0., 1.82, 1., .182)), loc=1, ncol=3, mode="expand", borderaxespad=0.,prop={'size':12},title="Files and Their Folder Name Plotted Below")
# 		pdf.savefig()
# 		plt.close()
		
# 		###########################
		
# 		#Create a bar plot of the slope of the baseline conductance
# 		fig = plt.figure()
# 		ax = fig.add_subplot(111)
# 		fig.set_size_inches(14.5, 10.5)
# 		ax.tick_params(labelsize=12)
# 		bars1 = []
# 		colors = cycle(["aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal", "yellow"])
		
# 		#Create bar graph in slopes
# 		for i in range ( len(x_axis) ):
# 			rects = ax.bar(x_axis[i], slopes[i], 0.35, color=next(colors))
# 			bars1.append( rects )
		
# 		#Set the range of x and add tick marks and tick labels
# 		ax.set_xlim(-width,len(x_axis) + 1 + width)
# 		ax.set_xticks(x_axis)
# 		xtickNames = ax.set_xticklabels(plantids)
# 		plt.setp(xtickNames, rotation=45, fontsize=14)
# 		ax.set_ylabel('Conduction',color='black', fontsize=14)
# 		ax.set_xlabel('Plantid',color='black', fontsize=14)
# 		plt.title('Slope of Baseline Conductance',y=1.08,fontsize=16)
# 		plt.axhline(0, color='black')
# 		plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
# 		plt.legend((bars1),(legend_headings),bbox_to_anchor=((0., 1.82, 1., .182)), loc=1, ncol=3, mode="expand", borderaxespad=0.,prop={'size':12},title="Files and Their Folder Name Plotted Below")
# 		pdf.savefig()
# 		plt.close()
# 		###########################

# 		#Compute Values for Exponential Growth and Decay 
# 		GrowthTaus, GrowthInitial,GrowthAsympote = [], [] , []
# 		DecayTaus, DecayInitial, DecayAsympote = [], [] , []

# 		#Loop through all the points (triplets)
# 		for i in range (len(CriticalPoints) ):
# 			triplet = map(float,CriticalPoints[i])
# 			phase1Tupl = (triplet[0],triplet[1])
# 			phase2Tupl = (triplet[1], triplet[2])
# 			plantid = plantids[i]

# 			#determine growth or decay came first in experiment	
# 			#Growth
# 			if phase1Tupl[0] < phase1Tupl[1]:
# 				#Add Growth and Decay Order Respectively
# 				GrowthTaus.append(Taus[i][0])
# 				DecayTaus.append(Taus[i][1])
# 				#Add growth from phase 1
# 				GrowthInitial.append(phase1Tupl[0])
# 				GrowthAsympote.append(phase1Tupl[1])
# 				#Add decay from phase 2
# 				DecayInitial.append(phase2Tupl[0])
# 				DecayAsympote.append(phase2Tupl[1])

# 			#Decay
# 			else:
# 				#Add Growth and Decay Order Respectively
# 				GrowthTaus.append(Taus[i][1])
# 				DecayTaus.append(Taus[i][0])
# 				#Add Decay from phase 1
# 				DecayInitial.append(phase1Tupl[0])
# 				DecayAsympote.append(phase1Tupl[1])
# 				#Add Growth from phase 2
# 				GrowthInitial.append(phase2Tupl[0])
# 				GrowthAsympote.append(phase2Tupl[1])
		
# 		###########################
# 		#Create Side by Side Plot for Tau Values
# 		fig = plt.figure()
# 		ax = fig.add_subplot(111)
# 		fig.set_size_inches(14.5, 10.5)
# 		ax.tick_params(labelsize=12)
# 		colors = cycle(["blue",  "maroon"])

# 		for i in range ( len(x_axis) ):
# 			rects = ax.bar(x_axis[i], GrowthTaus[i], 0.35, color=next(colors))
# 			rects1 = ax.bar(x_axis[i]+width, DecayTaus[i], 0.35, color=next(colors))

# 		#Set the range of x and add tick marks and tick labels
# 		ax.set_xlim(-width,len(x_axis) + 1 + width)
# 		ax.set_xticks(x_axis)
# 		xtickNames = ax.set_xticklabels(fileNamesOnly)
# 		plt.setp(xtickNames, rotation=75, fontsize=14)
# 		ax.set_ylabel('Tau Value',color='black',fontsize=14)
# 		ax.set_xlabel('File',color='black',fontsize=14)
# 		plt.title('Side by Side Plot Of Taus',fontsize=16)

# 		#Make the legend
# 		blue_patch = mpatches.Patch(color='blue', label='Exponential Growth')
# 		maroon_patch = mpatches.Patch(color='maroon', label='Exponential Decay')
# 		plt.legend(handles=[blue_patch,maroon_patch])	

# 		#Format and Save
# 		plt.tight_layout()
# 		pdf.savefig()
# 		plt.close()

# 		#######################
		
# 		#Create Side by Side Plot for Initial and Asympote values for Growth
# 		fig = plt.figure()
# 		ax = fig.add_subplot(111)
# 		fig.set_size_inches(14.5, 10.5)
# 		ax.tick_params(labelsize=12)
# 		colors = cycle(["blue",  "maroon"])
# 		for i in range ( len(x_axis) ):
# 			rects = ax.bar(x_axis[i], GrowthInitial[i], 0.35, color=next(colors))
# 			rects1 = ax.bar(x_axis[i]+width, GrowthAsympote[i], 0.35, color=next(colors))

# 		#Set the range of x and add tick marks and tick labels
# 		ax.set_xlim(-width,len(x_axis) + 1 + width)
# 		ax.set_xticks(x_axis)
# 		xtickNames = ax.set_xticklabels(fileNamesOnly)
# 		plt.setp(xtickNames, rotation=75, fontsize=14)
# 		ax.set_ylabel('Conductance Value',color='black',fontsize=14)
# 		ax.set_xlabel('File',color='black',fontsize=14)
# 		plt.title('Significant Exponential Growth Values Used to Calculate Tau',fontsize=16)

# 		#Make the legend
# 		blue_patch = mpatches.Patch(color='blue', label='Initial Value')
# 		maroon_patch = mpatches.Patch(color='maroon', label='Asymptote Value')
# 		plt.legend(handles=[blue_patch,maroon_patch])	

# 		#Format and save
# 		plt.tight_layout()
# 		pdf.savefig()
# 		plt.close()

# 		#######################
		
# 		#Create Side by Side Plot for Initial and Asympote values for Decay
# 		fig = plt.figure()
# 		ax = fig.add_subplot(111)
# 		fig.set_size_inches(14.5, 10.5)
# 		ax.tick_params(labelsize=12)
# 		colors = cycle(["blue",  "maroon"])
# 		for i in range ( len(x_axis) ):
# 			rects = ax.bar(x_axis[i], DecayInitial[i], 0.35, color=next(colors))
# 			rects1 = ax.bar(x_axis[i]+width, DecayAsympote[i], 0.35, color=next(colors))

# 		#Set the range of x and add tick marks and tick labels
# 		ax.set_xlim(-width,len(x_axis) + 1 + width)
# 		ax.set_xticks(x_axis)
# 		xtickNames = ax.set_xticklabels(fileNamesOnly)
# 		plt.setp(xtickNames, rotation=75, fontsize=14)
# 		ax.set_ylabel('Conductance Value',color='black',fontsize=14)
# 		ax.set_xlabel('File',color='black',fontsize=14)
# 		plt.title('Significant Exponential Decay Values Used to Calculate Tau',fontsize=16)

# 		#Make the legend
# 		blue_patch = mpatches.Patch(color='blue', label='Initial Value')
# 		maroon_patch = mpatches.Patch(color='maroon', label='Asymptote Value')
# 		plt.legend(handles=[blue_patch,maroon_patch])	

# 		#Format and Save
# 		plt.tight_layout()
# 		pdf.savefig()
# 		plt.close()

# 		#######################

# 		#Create Side by Side Plot for Min and Max values for Each File
# 		fig = plt.figure()
# 		ax = fig.add_subplot(111)
# 		fig.set_size_inches(14.5, 10.5)
# 		ax.tick_params(labelsize=12)
# 		colors = cycle(["blue",  "maroon"])
# 		for i in range ( len(x_axis) ):
# 			rects = ax.bar(x_axis[i], min(map(float,conductance[i])), 0.35, color=next(colors))
# 			rects1 = ax.bar(x_axis[i]+width, max(map(float,conductance[i])), 0.35, color=next(colors))

# 		#Set the range of x and add tick marks and tick labels
# 		ax.set_xlim(-width,len(x_axis) + 1 + width)
# 		ax.set_xticks(x_axis)
# 		xtickNames = ax.set_xticklabels(fileNamesOnly)
# 		plt.setp(xtickNames, rotation=75, fontsize=14)
# 		ax.set_ylabel('Conductance',color='black',fontsize=14)
# 		ax.set_xlabel('File',color='black',fontsize=14)
# 		plt.title('Min and Max Conductance',fontsize=16)

# 		#Make the legend
# 		blue_patch = mpatches.Patch(color='blue', label='Min Conductance')
# 		maroon_patch = mpatches.Patch(color='maroon', label='Max Conductance')
# 		plt.legend(handles=[blue_patch,maroon_patch])	

# 		#Format and Save
# 		plt.tight_layout()
# 		pdf.savefig()
# 		plt.close()


#########################
#########################
#old possibly broken code
		#Create Side by Side Plot for Initial and Asympote values for Decay

		# #Create third Bar Graph
		# # Number of clusters
		
		# GrowthTaus = []
		# DecayTaus = []
		# #Loop through all the points (triplets)
		# for i in range (len(CriticalPoints) ):
		# 	triplet = CriticalPoints[i]
		# 	phase1Tupl = (triplet[0],triplet[1])
		# 	phase2Tupl = (triplet[1], triplet[2])
		# 	plantid = plantids[i]

		# 	#determine growth or decay came first in experiment
		# 	behavior = 0
		# 	trend = 0
		# 	#Growth
		# 	if phase1Tupl[0] < phase1Tupl[1]:
		# 		GrowthTaus.append(Taus[i][0])
		# 		DecayTaus.append(Taus[i][1])
		# 		# behavior = "Inverse Exp. Decay Parameters"
		# 		# trend = 1
		# 	#Decay
		# 	else:
		# 		GrowthTaus.append(Taus[i][1])
		# 		DecayTaus.append(Taus[i][0])
		# 		# behavior = "Exp. Decay Parameters"
		# 		# trend = -1

		# 	fig = plt.figure()


		# 	###########################Make plot for Initial Point and Asymptote###########################
		# 	#create the first figure
		# 	ax = fig.add_subplot(131)
		# 	ax.set_ylabel('Conductance')
		# 	ax.set_title( behavior+ "\n",fontsize=10)
		
		# 	#Define the two bars for the graph
		# 	rect1 = ax.bar(x_axis[0] + width, float(phase1Tupl[0]), color='r')
		# 	rect2 = ax.bar(x_axis[1] + width, float(phase1Tupl[1]), color='g')

		# 	#Add the x-axis details
		# 	xtickNames = ax.set_xticklabels(['Initial Value','Asymptote'])
		# 	ax.set_xticks( [x_axis[0] + 0.75, x_axis[1] + 0.75 ] )
		# 	plt.setp(xtickNames, fontsize=10)

		# 	#Find whether decay or inverse exponential decay comes first
		# 	if behavior == "Inverse Exp. Decay Parameters":
		# 		behavior = "Exp. Decay Parameters"
		# 	else:
		# 		behavior = "Inverse Exp. Decay Parameters"

		# 	###########################Make plot for Initial Point and Asymptote###########################
		# 	#Create the second figure
		# 	ax = fig.add_subplot(132)
		# 	ax.set_title( legend_headings[i] + '\n' + behavior+ "\n",fontsize=10)
		# 	#Create the next two bars for the second bar graph
		# 	rect1 = ax.bar(x_axis[0] + width, float(phase2Tupl[0]), color='r')
		# 	rect2 = ax.bar(x_axis[1] + width, float(phase2Tupl[1]), color='g')
		# 	#Add x-axis bar graphs
		# 	xtickNames = ax.set_xticklabels(['Initial Value','Asymptote'])
		# 	ax.set_xticks( [x_axis[0] + 0.75, x_axis[1] + 0.75 ] )
		# 	plt.setp(xtickNames, fontsize=10)

		# 	###########################Make plot for Tau###########################
		# 	#Create third figure
		# 	ax = fig.add_subplot(133)
		# 	ax.set_title( "Tau" + "\n",fontsize=10)
		# 	#Create the next two bars for the third bar graph
		# 	rect1 = ax.bar(x_axis[0] + width, Taus[i][0] , color='b')
		# 	rect2 = ax.bar(x_axis[1] + width, Taus[i][1] , color='b')
		# 	#Add X-axis Details
		# 	order = []
		# 	if trend == -1:
		# 		order = ['Inverse Exp.','Exp.']
		# 	else:
		# 		order = ['Exp.','Inverse Exp.']
		# 	xtickNames = ax.set_xticklabels(order)
		# 	ax.set_xticks( [x_axis[0] + 0.75, x_axis[1] + 0.75 ] )
		# 	plt.setp(xtickNames, fontsize=10)
			
		# 	#Save the figure to the pdf
		# 	pdf.savefig()
		# 	plt.close()
		# # 	###########################


			









