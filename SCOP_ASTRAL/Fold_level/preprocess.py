f = open('folds.txt','r')
files = f.readlines()
f.close()

for FAM_ID in files:
	print FAM_ID.strip()
	f=open('./folds/'+FAM_ID.rstrip(),'r')
	data=f.readlines()
	f.close()

	f=open(FAM_ID.rstrip()+'.txt','w')
	text = ''

	for line in data:
		if line[0] =='>':
			continue
		else:
			text+=line.rstrip()


	f.write(text)
	f.close()
