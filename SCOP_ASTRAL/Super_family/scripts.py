##for cumulating the supfam wise families & count the number of protein sequences
fam = {}
for line in data:
    if line[0]=='>':
        words = line.split(' ')
        r = words[1].rfind('.');supfam = words[1][0:r+1];
        if supfam not in fam:
            fam[supfam]={}
            fam[supfam][words[1]]=1
        else:
            count = fam[supfam].get(words[1],0)
            fam[supfam][words[1]]=count+1


for item in fam:
	f.write(item+'\n')
	for temp in fam[item]:
		f.write(temp+' '+str(fam[item][temp])+'\t')
	f.write('\n')


FAM_ID='b.1.1'
f=open(FAM_ID,'r')
data=f.readlines()
f.close()

curr_fam = ''
fam=''
f=open(fam+'.txt','w')
text = ''

for line in data:
	if line[0] =='>':
		words = line.split(' ')
        	fam = words[1]
		if fam == curr_fam:
			continue
		else:
			curr_fam = fam
			f.write(text)
			f.close()
			text = ''
			f=open(fam+'.txt','w')
	else:
		text+=line.strip()


f.write(text)
f.close()
