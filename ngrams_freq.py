import pickle
import copy


f = open('combined_biotext.txt','r');
data =  f.readline();
f.close();


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
f=open('bio_ngram_'+str(n),'wb')
pickle.dump(ngrams_dict,f)
f.close()

