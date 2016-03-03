files = ['a','b','c','d','e','f','g']

for FAM_ID in files:
	f=open(FAM_ID,'r')
	data=f.readlines()
	f.close()

	f=open(FAM_ID+'.txt','w')
	text = ''

	for line in data:
		if line[0] =='>':
			continue
		else:
			text+=line.rstrip()


	f.write(text)
	f.close()
