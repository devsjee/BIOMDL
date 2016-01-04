import pickle
import copy

data = ''
FNAME = 'PS01199_867'

with open('./'+FNAME+'/'+FNAME+'.fasta','r') as f:
	temp =  f.readline()
	while len(temp)>0:
		if temp[0] == '>':
			print '>'
			temp =  f.readline()
			continue
		temp = temp.strip()
		data = data+temp
		temp =  f.readline()

f=open('./'+FNAME+'/'+FNAME+'.txt','w')
f.writelines(data)
f.close()


n = 1
ngrams_dict = dict()
for j in range(len(data) - n + 1):
        temp = data[j:j + n]
	if temp in ngrams_dict:
		ngrams_dict[temp] +=1
	else:
		ngrams_dict[temp] =1

print ngrams_dict
print len(ngrams_dict)
f=open('./'+FNAME+'/'+FNAME.split('_')[0]+'_ngram_'+str(n),'wb')
pickle.dump(ngrams_dict,f)
f.close()


