f=open('astral-scope2.05.fa.txt','r')
data = f.readlines()
f.close()

curr_class = ''
cls=''
f=open(cls+'.txt','w')
text = ''

for line in data:
	if line[0] =='>':
		words = line.split(' ')
		r = words[1].find('.'); cls = words[1][0:r+1];
        	
		if cls == curr_class:
			continue
		else:
			curr_class = cls
			f.write(text)
			f.close()
			text = ''
			f=open(cls+'.txt','w')
	else:
		text+=line.strip()


f.write(text)
f.close()
