f=open('astral-scope2.05.fa.txt','r')
data = f.readlines()
f.close()

curr_fold = ''
fold=''
f=open(fold+'.txt','w')
f1=open('fold_level_test.txt','w')
text = ''
count = 0
count_t = 0
test =''

for line in data:
	if line[0] =='>':
		words = line.split(' ')
		r = words[1].find('.',2); fold = words[1][0:r];
        	
		if fold == curr_fold:
			count+=1
			if count%10 == 0:
				test+=line
				count_t+=1
			else:
				text+=line

			continue
		else:
			#print 'fold ',curr_fold,' has ',str(count),' members'
			#print 'fold ',curr_fold,' has ',str(count_t),' test members'
			curr_fold = fold[:]
			f.writelines(text)
			f.close()
			#f1.writelines(test)
			#f1.close()
			text = line
			#test = ''
			count =1
			count_t = 0
			f=open(fold,'w')
			print fold
			#f1=open(cls+'_test.txt','w')
	else:
		if count%10 == 0:
			test+=line
		else:
			text+=line


f.writelines(text)
f.close()
f1.writelines(test)
f1.close()
