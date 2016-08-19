import csv
import sys

filename = sys.argv[1]

## read file...:
with open(filename,'rU') as inputfile:
	reader_input = csv.reader(inputfile,dialect=csv.excel_tab)
	datalist_input=[]
	for row in reader_input:
		rowlist=[]
		for col in row:
			rowlist.append(col)
		datalist_input.append(rowlist)

completelist_input=[]
for row in range(len(datalist_input)):
	str=datalist_input[row][0].split(';')
	completelist_input+=[str]

## change format of input
sorted_input_list=[]
for row in range(len(completelist_input)):
	rowlist=[]
	#determine whether it's TUBE or PLATE
	well_str = completelist_input[row][1]
	if(well_str=='TUBE'):
		rowlist.append(completelist_input[row][0])
		# in this case, the identifier is the tube-name, i.e. column 2
		rowlist.append('TUBE')
		ident_list = completelist_input[row][2].split('_')
		rowlist.append(ident_list[1])
		rowlist.append(ident_list[0])
		sorted_input_list.append(rowlist)
	else: ## not TUBE, can still be empty line...
		if(len(completelist_input[row][2])>0):	
			rowlist.append(completelist_input[row][0])
			rowlist.append(completelist_input[row][1])
			curr_well = completelist_input[row][2]
			#letter = curr_well[0]
			#number = curr_well[1:len(curr_well)]
			rowlist.append(curr_well[0])
			rowlist.append(curr_well[1:len(curr_well)])
			sorted_input_list.append(rowlist)
	

sorted_input_list.sort(key=lambda l:(l[1],l[2],int(l[3])))

## write sorted list to file:
with open('output_sorted.csv','wb') as file_output:
	writer = csv.writer(file_output,delimiter=';')
	writer.writerows(sorted_input_list)

## create pipetting scheme:
pipetting_scheme=[]
old_plate=sorted_input_list[0][1]
old_well=sorted_input_list[0][2]
row_pipetting_scheme=[]
row_pipetting_scheme.append(old_plate)
row_pipetting_scheme.append(old_well)
row_pipetting_scheme.append(sorted_input_list[0][3])
for i in range(1,len(sorted_input_list)):
	curr_plate = sorted_input_list[i][1]
	curr_well = sorted_input_list[i][2]
	if(curr_well!=old_well):
		pipetting_scheme.append(row_pipetting_scheme)
		row_pipetting_scheme=[]
		row_pipetting_scheme.append(curr_plate)
		row_pipetting_scheme.append(curr_well)
		row_pipetting_scheme.append(sorted_input_list[i][3])
	else:
		row_pipetting_scheme.append(sorted_input_list[i][3])
	
	old_plate=curr_plate
	old_well=curr_well

pipetting_scheme.append(row_pipetting_scheme)


## write pipetting scheme to file:
with open('output_ps.csv','wb') as file_output:
	writer = csv.writer(file_output,delimiter=';')
	writer.writerows(pipetting_scheme)



