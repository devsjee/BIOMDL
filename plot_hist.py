#ensure that the file has lines of format 'segment<splace/tab> count/freq'
fname= 'output2.txt'

data = []
hist = {}

with open(fname,'r') as f:
	data = f.readlines()

for item in data:
	temp = item.rstrip()
	temp = temp.split('\t')
	count = temp[1]	
	hist[count] = hist.get(count,0)+ 1

with open('hist_plot.txt','w') as f:
	for item in hist:
		f.writelines(str(item)+'\t'+str(hist[item])+'\n')
