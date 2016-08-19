#To be able to read csv formated files, we will first have to import the
#csv module.
import csv
import sys
from operator import itemgetter

def find_value(l,elem):
	for row, i in enumerate(l):
		try:
			column=i.index(elem)
		except ValueError:
			continue
		return row, column
	return -1

def find_all_values(l,index_column,elem):
	times_found=0
	index_list=[]
	for row in range(0,len(l)):
		if(l[row][index_column]==elem):
			times_found+=1
			index_list.append(row)
	return index_list
		
		

# start by opening the list of oligos retrieved from caDNAno....
filename = sys.argv[1]

with open(filename,'rU') as inputfile:
	reader_input = csv.reader(inputfile,dialect=csv.excel_tab)
	datalist_input=[]
	completelist_input=[]
	for row in reader_input:
		rowlist=[]
		for col in row:
			rowlist.append(col)
		datalist_input.append(rowlist)
for row in range(len(datalist_input)):
	str=datalist_input[row][0].split(';')
	completelist_input+=[str]

with open('//Users//christianwachauf//Dropbox//Promotion//LetzteExperimente//Polymerisierungskinetik//24hb//comp_oligo_list_24hb.csv', 'rU') as f:
    reader = csv.reader(f,dialect=csv.excel_tab)
    datalist=[]
    completelist=[]
    for row in reader:
    	    rowlist = []
    	    #print row
    	    for col in row:
    	    	    rowlist.append(col)
    	    datalist.append(rowlist)

for row in range(len(datalist)):	    
	str=datalist[row][0].split(';')
	completelist+=[str]

## create three lists:
## 1. for input-sequences that were found exactly once
## 2. for input-sequences that were found multiple times
## 3. for input-sequences that were not found at all....

unique_sequ_list=[]
multiple_sequ_list=[]
empty_sequ_list=[]
outputlist = sorted(completelist,key=itemgetter(3))
## loop over all input-sequences
for row in range(1,len(completelist_input)):
	res = find_all_values(outputlist,3,completelist_input[row][2])
	if(len(res)==0):
		empty_sequ_list.append(row)
	elif(len(res)>1):
		multiple_sequ_list.append([row,res])
	else:
		unique_sequ_list.append([row,res[0]])
	

## make table that sums up the results:


final_list = []
list_entry=[]
## append the unique matches
final_list.append(["unique matches: "])
for i in unique_sequ_list:
	list_entry=[]
	list_entry.append(completelist_input[i[0]][2]);
	for column in outputlist[i[1]]:
		list_entry.append(column)
	final_list.append(list_entry)


## append the multiple matches:
final_list.append(["multiple matches: "])

for i in multiple_sequ_list:
	list_entry=[]
	list_entry.append(completelist_input[i[0]][2])
	for j in i[1]:
		for column in outputlist[j]:
			list_entry.append(column)
	final_list.append(list_entry)
		
## append the none-matches:
final_list.append(["no matches: "])
for ind in empty_sequ_list:
	list_entry=[]
	list_entry.append(completelist_input[ind][2])
	final_list.append(list_entry)
	
with open('output.csv','wb') as file_output:
	writer = csv.writer(file_output,delimiter=';')
	writer.writerows(final_list)


