import pickle
import copy

data = ''

with open ('PS01162.txt','r') as f:
	temp =  f.readline()
	while len(temp)>0:
		temp = temp.strip()
		data = data+temp
		temp =  f.readline()


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
f=open('PS01162_ngram_'+str(n),'wb')
pickle.dump(ngrams_dict,f)
f.close()


