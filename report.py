#This report will compare the output2 files in the given folders and print a report
#of the common and disjoint parts within it.

folders={'PS51527_43','PS51482_80'}

common = {}

for folder in folders:
	with open('./'+folder+'/output2.txt','r') as f:
		data = f.readlines()

	for line in data:
		temp = line.rstrip()
		temp = temp.split('\t')
		freq = temp[1]	
		segment = temp[0]
		count  = common.get(segment,0)
		if count == 0:
			common[segment] = [freq]
		else:
			common[segment].append(freq)

common = common.items()
common.sort(key=lambda x:len(x[0]))

with open('common.txt','w') as f:
	for item in common:
		if len(item[1]) > 1:
			f.write(item[0]+'\t')
			print item[1]
			for num in item[1]:
				f.write(str(num)+' ')
			f.write('\n')
	
