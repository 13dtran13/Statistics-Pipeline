import argparse
import numpy 
import os
from collections import defaultdict
from scipy import stats
import subprocess

#python parser_for_config.py ~/Documents/Research/Schroeder\ Research/Statistics-Pipeline/data/phenodata.txt

# Parse the input values of the command line
parser = argparse.ArgumentParser(description='Open the config file')
parser.add_argument('filename', type=str, help='The name of the config file (must be tab deliminated)')
args = parser.parse_args()

'''----------------------------------------------------------------'''
'''------------------------Helper Functions------------------------'''
'''----------------------------------------------------------------'''

'''
Add all files that are set to true into the data_Matrix for specific columns
data_Matrix is a 2d array
'''
def addToDataMatrix(MAIN_config):

	data_Matrix = []

	#Cluster all the input files based on a key
	#The key from the config file is plantid-cond1-cond2-CO2
	for row in MAIN_config:

		#Skip header and skip any file that has a load set to false
		if (row[8].lower() == "false" or row[0] == "plantid" or row[0] == ""):
			continue; 
		
		# Rename strings from row array, and time_string_array requires a check to see if it is empty
		plantid, cond1, cond2, CO2_string, folder_and_file, instrument = row[0], row[1], row[2], row[3], row[5] + "/" + row[6], row[7]
		time_string_array = []
		if (row[4] != "" ):
			time_string_array = row[4].split(';')
		else: 
			time_string_array = {0}
		
		# Insert into 0 index and make a temp array for management
		array_to_insert_into_matrix = [folder_and_file]
		
		#Get the colums on data for cond1, cond2 and CO2R and insert into temp_array
		array_to_insert_into_matrix.append( ExtractOneCondtion(folder_and_file, cond1, instrument) )
		array_to_insert_into_matrix.append( ExtractOneCondtion(folder_and_file, cond2, instrument) )
		array_to_insert_into_matrix.append( ExtractOneCondtion(folder_and_file, "CO2R", instrument) )

		#Insert plantid
		array_to_insert_into_matrix.append(plantid)

		#Get the int arrays of CO2 and Time values both deliminated with semi collections			
		#Remove any quotations and cast CO2 values to ints
		CO2_int = split_CO2_String_Array(CO2_string)
		array_to_insert_into_matrix.append(CO2_int)

		time_int = []
		if (time_string_array[0] == 0 or time_string_array[0] == "" or time_string_array[0] == "none"):
			time_int.append( -1 )
		else: 
			for value in time_string_array:
				value = time_int.append( int(  value.replace('"',"").replace("'","")  ) )
		array_to_insert_into_matrix.append(time_int)
		
		#Insert condition strings
		array_to_insert_into_matrix.append(cond1)
		array_to_insert_into_matrix.append(cond2)
		data_Matrix.append(array_to_insert_into_matrix)

		if (instrument == "6400"):
			array_to_insert_into_matrix.append( ExtractOneCondtion(folder_and_file, "Time", instrument) )
		if (instrument == "6400XT"):
			array_to_insert_into_matrix.append( ExtractOneCondtion(folder_and_file, "FTime", instrument) )
		array_to_insert_into_matrix.append( ExtractOneCondtion(folder_and_file, "Ci", instrument) )
		array_to_insert_into_matrix.append( ExtractOneCondtion(folder_and_file, "H2OR", instrument) )
		array_to_insert_into_matrix.append( ExtractOneCondtion(folder_and_file, "Cond", instrument) )
	return data_Matrix

'''
Helper method to extract one specific column from one specific file 
and return that data array
'''
def ExtractOneCondtion( folder_and_file, cond, instrument ):

	#Find the absolute path and find the length of the config file
	path = os.path.abspath(args.filename)
	num = len(os.path.basename(args.filename))

	#Append the path to the file in order to open file
	abs_path_file = path[:-num]+folder_and_file

	#if the instrument was 6400Xt and the current file is from 6400XT
	if (instrument == "6400XT"):

		#Iterate through file and get header
		header_array, cond_array, array_to_return = [], [], []
	
	#find the header line
		with open(abs_path_file) as file:
			for line in file:
				if ( line[1:4] == "Obs" ):		
					header_array = line.split("\t")
				if ( line[0] != "<" and line[0] != '"' ):
					cond_array.append(line.split("\t"))
		cond_array.pop(0)
		
		#Get the column number associated with the provided input values
		column_number = header_array.index('"'+str(cond)+'"')
		
		for subarray in cond_array:
			rawData = subarray[column_number].rstrip()
			array_to_return.append(rawData)
		return array_to_return

	#if the instrument was 6400 and the current file is from 6400XT
	if (instrument == "6400"):

		#Get the column titles (strings) and get the line to skip to
		array_col_name = []
		lineToStartOn = 0
		with open(abs_path_file) as infile:
			for line in infile:
				if (line[1:4] == "Obs"):
					array_col_name = line.split(',')
					break
				lineToStartOn = lineToStartOn + 1

		#Get the column number associated with the provided input values
		column_number = array_col_name.index('"'+str(cond)+'"')
		
		cond_array = numpy.loadtxt(abs_path_file,dtype=str,delimiter=',',skiprows=lineToStartOn+1,usecols=(column_number,))
		return cond_array

'''
Takes in Main_config and clusters all files in config based on plantid-cond1-cond2-CO2
and returns a dictionary where keys are the plantid-cond1-cond2-CO2 and values are
all values in that cluster	
'''
def ClusterConfigFiles(MAIN_config):
	
	#Create a dictionary to cluster files according
	cluster_files = defaultdict(list)

	#Cluster all the input files based on a key
	#The key from the config file is plantid-cond1-cond2-CO2
	for row in MAIN_config:
		#Skip header and skip any file that has a load set to false
		if (row[8].lower() == "false" or row[0] == "plantid" or row[0] == ""):
			continue; 
		else:
			#Concatenate the plantid,cond1,cond2,CO2 to make a unique key
			key = str(row[0]) + "-" + str(row[1]) + "-" + str(row[2]) + "-" + str(row[3])
			#Concatenate the folder and the file together 
			value = row[5] + "/" + row[6]
			#Add the key to the dictionary and all the files associated with it
			cluster_files[key].append(value)
	return cluster_files

'''
Given a string that has CO2 levels separated by semi-colons, return an array of the CO2 ints
'''
def split_CO2_String_Array(CO2_string):
	CO2_int = []
	CO2_string_array = CO2_string.split(";")
	#Remove excess quotes
	for value in CO2_string_array:
		CO2_int.append( int(  value.replace('"',"").replace("'","")  )  )
	return CO2_int

'''
Find the data in the matrix that matches the provided key
'''
def getData(Fold_File, data_Matrix):
	for array in data_Matrix:
		if (array[0] == Fold_File):
			return array

'''
Find index of the nearest value in a time array
'''
def findNearestTimeIndex( value, array ):
	return_index = 0
	index = 0
	for sec in array:
		if (float(sec) > value):
			break
		if ( ( value - float(sec) ) > 0 ):
			return_index = index
		index = index + 1
	return return_index

'''
Split cond array using CO2 values and returns array of indexes that are each separate point
'''
def splitArray( CO2R_array, levels_CO2_array):
	return_index_array = [0]

	temp_index = 5; 
	# loop through each CO2 argument
	for curr_CO2_arg in levels_CO2_array:
		# loop through the CO2 data array and find the index that matches 
		for i in range( temp_index,len(CO2R_array) - 6 ):
			curr_co2_data = float(CO2R_array[i])
			if ( abs(float(curr_CO2_arg) - curr_co2_data) > 10 ):
				return_index_array.append(i)
				temp_index = i + 5
				break
	return return_index_array

'''
Call a shell command while in script
'''
def callShellCommand(input):
	subprocess.Popen(input,shell = True).wait()

'''

'''
def parseStaticsForHistTable(cluster_files, data_Matrix):

	plotTable = []
	
	# loop through each clustering and get the common id 
	# and the series of files 
	for key, value in cluster_files.iteritems():
		id_array = key.split("-")
		plantid = id_array[0]
		cond1 = id_array[1]
		cond2 = id_array[2]
		CO2_int_array = split_CO2_String_Array( id_array[3] )
		
		#for each file parse the Co2 and time parameters
		for file in value:
			data_array_per_file = getData(file, data_Matrix)
			
			time_periods = data_array_per_file[6]
			exp_time = data_array_per_file[9]
			stored_indexes = [0]
			CO2R_array = data_array_per_file[3]
			levels_CO2_array = data_array_per_file[5]
			conduction_array = data_array_per_file[12]
			#If no time was provided
			if ( time_periods[0] == -1 ):
				stored_indexes = splitArray( CO2R_array, levels_CO2_array)
				stored_indexes.append(len(CO2R_array) -1 )
			
			#Else if time was provided
			else:
				
				#Indexes array referring to the split of data with time data and temporary variable
				previous_sec = float(0)
				
				#For loop to find indexes for each time setting
				for i in range(0 , len(time_periods)-1):
					
					#The current instrument time setting duration (additive)
					cur_period = time_periods[i]
					
					#Current seconds accounted from previous time slot as well and update previous seconds
					seconds = float(cur_period*60) + float(previous_sec)
					previous_sec = seconds

					#Find the index of time-data that is closest to the purposed time value
					index = findNearestTimeIndex(float(seconds),exp_time)
					stored_indexes.append(index)

				#Add the last index into array
				stored_indexes.append(len(exp_time)-1)
			
			plotTable.append(buildHistTable(stored_indexes,conduction_array,exp_time,data_array_per_file))
	return plotTable
'''
Find Histogram Table
(plantid,0) (BLcond,1) (LinR([Blcond],2) ) ( array of P/Cond,3 ) (value of max, 4) 
Input: a plantid, array of stored indexes, conductance array,
Output: An array to write that should be written to file
'''
def buildHistTable(indexes_list,conduction_array,time_array,array_data_file):
	
	#array that will hold the separate conduction_array 
	separated_data, separated_time, plotTable = [],[],[]
	for i in range ( 1, len(indexes_list) ):
		placeholder,time_hold = [], []
		for k in range( indexes_list[i-1], indexes_list[i]):
			placeholder.append(conduction_array[k])
			time_hold.append(time_array[k])
		separated_time.append(time_hold)
		separated_data.append(placeholder)
	
	#Add plantid with folder
	plotTable.append(array_data_file[0])
	#Add baseline conductance
	baseline_data = numpy.array(separated_data[0],dtype=numpy.float64)
	plotTable.append(numpy.mean(baseline_data))
	#Add the slop the of line, after computing linear regression
	x, y = numpy.array(separated_time[0],dtype=numpy.float64), numpy.array(separated_data[0],dtype=numpy.float64)
	slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
	plotTable.append(slope)

	#Add max values for each time period
	max_array = []
	for time_period in separated_data:
		max_array.append(max(time_period))
	plotTable.append(max_array)
	return plotTable

'''
Print the entire data matrix in a text art version
'''
def toString(data_Matrix):
	print "\n\n\n"
	print "                                                           Table Values For Each File                                                                    "
	print "---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
	print "|\tFold-File\t|\t[]cond1\t|\t[]cond2\t|\t[]CO2\t|\tplantid\t|\t[]L.Co2\t|\t[]Time\t|\tcond1\t|\tcond2\t|\t[]time_exp\t|\t[]ci_exp\t|\t[]H2OR_exp\t|"
	print "---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"	
	print "|\t0 index\t\t|\t1 index\t|\t2 index\t|\t3 index\t|\t4 index\t|\t5 index\t|\t6 index\t|\t7 index\t|\t8 index\t|\t 9 index\t|\t 10 index\t|\t 11 index\t|"
	print "---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
	print "_________________________________________________________________________________________________________________________________________________________________________________"

	for array in data_Matrix:
		if ( array[6][0] != "-1" ):
			print "|\t"+array[0][16:30] +"\t|\t"+ str(len(array[1])) +"\t|\t"+ str(len(array[2])) +"\t|\t"+ array[3][0] +"\t|\t"+ array[4] +"\t|\t"+ str(array[5][0]) +"\t|\t"+ str(array[6][0]) +"\t|\t"+ array[7] +"\t|\t"+ array[8] + "\t|\t" + str(len(array[9])) + "\t\t|"
		else: 
			print "|\t"+array[0][16:30] +"\t|\t"+ str(len(array[1])) +"\t|\t"+ str(len(array[2])) +"\t|\t"+ array[3][0] +"\t|\t"+ array[4] +"\t|\t"+ str(array[5][0]) +"\t|\t"+ "none" +"\t|\t"+ array[7] +"\t|\t"+ array[8] + "\t|\t" + str(len(array[9])) + "\t\t|"			
		print "_________________________________________________________________________________________________________________________________________________________________________________"
	print "\n\n\n"

'''-------------------------------------------------------------'''
'''------------------------Main Function------------------------'''
'''-------------------------------------------------------------'''

def main():
	#Remove any path strings attached to the input file name
	file_title=os.path.basename(args.filename)
	path = os.path.abspath(args.filename)
	num = len(os.path.basename(args.filename))
	abs_path_file = path[:-num]

	#Save the entire textfile as a numpy ndarray
	MAIN_config = numpy.loadtxt(args.filename,dtype=str,delimiter='\t',skiprows=0)
	# MAIN_config = numpy.loadtxt(args.filename,dtype=str,delimiter='\t',skiprows=0 , usecols = (1,4,5))
	#Load all necessary columns into the data_matrix for each file
	data_Matrix = addToDataMatrix(MAIN_config)

	#Cluster all files accordingly
	cluster_files = ClusterConfigFiles(MAIN_config)

	toString(data_Matrix)

	histTable = parseStaticsForHistTable(cluster_files, data_Matrix)
	
	for array in histTable:
		print array

		# file_count = len(value) + 1
		# counter = 1
		# #Create a figure for this clustering that will hold everything

		# fig = plt.figure(figsize=(15, file_count*10 ))

		# multiplot = fig.add_subplot(file_count,1,counter)
		# count = counter + 1
		# plotter.simpleMultiScatterPlot(data_Matrix, fig, value, multiplot)


		
		# '''
		# Finished making scatter plots
		# Text is parse each individual file with 
		# '''

		# plt.savefig(key+".pdf")
			
# Main Function
if __name__ == "__main__":
    main()
