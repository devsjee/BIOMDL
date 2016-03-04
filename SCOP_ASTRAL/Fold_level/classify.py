import pickle
import math
import copy
from sklearn.metrics import confusion_matrix

FOLDER = './'
TEST_FNAME ='fold_level_test.txt'
FAM_NAMES = ['a.1','a.2','a.3','a.4','a.24','a.29','a.39','a.45','a.60','a.118','b.6','b.29','b.36','b.40','b.42','b.60','b.82','b.121','c.2','c.3','c.14','c.108','d.3','d.79','d.92','d.129','e.3','f.23','g.39']


DLG_stored = []
freq_total = {}
freq = dict()
corpus = ''
corpus_total = {}
test = ''
X = 0
label_pred = []
label_actual = []

def load_freq():
	global freq_total 
	for family in FAM_NAMES:
		fname = FOLDER+family+'.txt'
		f = open(fname,'r');
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

		freq_total[family] = ngrams_dict
		
def load_corpus():
	global corpus_total
	for family in FAM_NAMES:
		fname = FOLDER+family+'.txt'
		f = open(fname,'r');
		data =  f.readline();
		f.close();
		corpus_total[family]= copy.deepcopy(data)	

def load_data(family,test):
	global freq,freq_total,corpus,corpus_total,X

	freq = freq_total[family]
	corpus = corpus_total[family]
	X = len(corpus)

def corpusDL():
    global freq

    total =0
    for key,value in freq.iteritems():
	total += value * (math.log(value,2) - math.log(X,2))
    total = -1*total
    return total


'''def occurrences(string, sub):
    count = start = 0
    while True:
        start = string.find(sub, start) + 1
        if start > 0:
            count+=1
        else:
            return count
'''

def occurrences(sentence,substring):
    return sentence.count(substring)

def DLG(s):
	global freq,corpus,X

	suffix = len(s)
	cs = occurrences(corpus,s)
	n = X - cs*suffix + cs + suffix + 1
	total =0
	for key,value in freq.iteritems():
		csx = occurrences(s,key)
   		#print '{} occurs {} times in {}'.format(key,csx,s)
		cx = value - cs*csx + csx
		#print 'cs '+str(cs)+ ' value ' +str(value)+' cx '+str(cx)+' csx '+str(csx)+' n '+str(n)
		total += cx * (math.log((cx/(1.0*n)),2))
		
	total += cs* (math.log(cs,2) - math.log(n,2))
	total = -1*total
    
	dlg = (DL - total)/cs
    #print 'DLG of {} is {}'.format(s,dlg)
   
	return dlg  

def OpSeg(U):
	global corpus
	n = len(U)
	OS = []
	for k in range(0,n):
		if k>30:
			OS[k-30][:]=[]

		OS.append([])

		if k>0:
            		OS[k][:]= []
	    		OS[k] = copy.deepcopy(OS[k-1])
	    		OS[k].append(U[k])
		        DLG_stored.append(DLG_stored[k-1])
		else:
			OS[k][:]=[]
		 	OS[k].append(U[k])
	    		DLG_stored.append(0)


		'''print 'k value is ',k
		print 'OS is ', OS
		print 'DLG stored is ',DLG_stored'''

		for j in range(k,-1,-1):
			if j < k-25:
	        		break
			ngram = U[j:k+1]
            #print ngram
			if occurrences(corpus,ngram)<2:
            #print 'breaking\n'
				break
			if len(ngram) == 1 :
				dlgain = DLG_stored[j-1]
			if j>0:
				dlgain = DLG_stored[j-1] + DLG(ngram)
			else:
				dlgain = DLG(ngram)

			'''print DLG_stored
	            print 'new DL', dlgain
	            print 'DLG_stored is ',DLG_stored[k]'''
			if (dlgain >DLG_stored[k]) and j>0:
				OS[k][:] = []
				OS[k] = copy.deepcopy(OS[j-1])
				OS[k].append(ngram)
				#print 'OS[{}] is now assigned {}'.format(k,OS[k])
				DLG_stored[k] = copy.deepcopy(dlgain)
			elif (dlgain> DLG_stored[k]) and j==0:
				OS[k][:]=[]
				OS[k].append(ngram)
				DLG_stored[k] = copy.deepcopy(dlgain)
		                #print 'OS[{}] is now assigned {}'.format(k,OS[k])

	#print 'n =',str(n),'	len of DLG_STORED ',len(DLG_stored)		 
	return OS[n-1],DLG_stored[n-1]


  


def process_test(TEST_FNAME):
	f=open( FOLDER+TEST_FNAME,'r')
	data=f.readlines()
	f.close()

	curr_fam = ''
	fam=''
	text = ''
	test = []
	for line in data:
		if line[0] =='>':
			if fam =='':
				words = line.split(' ')
				r = words[1].find('.',2); 
		       		fam = words[1][0:r]
				continue
			else:
				test.append([fam,text])
				text = ''
				words = line.split(' ')
        			r = words[1].find('.',2); 
		       		fam = words[1][0:r]
		
		else:
			text+=line.strip()


	test.append([fam,text])
	#print test
	return test



load_freq()
load_corpus()

test_list = process_test(TEST_FNAME)
print len(test_list)

correct = 0
total = 0
fout = open( FOLDER+'OUTPUTS/output.txt','a') 
for item in test_list:
	test_case = item[0]
	test = item[1]
	
	max_compression = -1000
	label = []
	total +=1
	fout.write('\n\nActual Fold : '+test_case+'\t'+test+'\n')
	for family in FAM_NAMES:
		
		load_data(family,test)
		
		#print 'len of corpus ',family,' ',str(X)

		DL = corpusDL()
		#print 'DL is ',str(DL)

		output,compression = OpSeg(test)
		#print output
		fout.write('\nFold '+family+' gives following output\n')
		for i in range(len(output)):
			#f.write("[")
			fout.write(output[i]+ ', ')
			#f.write("] ")
		fout.write('\t Compression '+str(compression))
		print 'Fold ',str(family),'  compression ',str(compression)
		if compression > max_compression:
			max_compression = compression
			label = family
		
	
		DLG_stored = []
		freq = {}
	
	print 'Predicted : '+str(label)+'	Actual : '+test_case
	print  test_case == label
	if test_case == label:
		correct+=1.0
	label_pred.append(label)
	label_actual.append(test_case)

print 'Correct : ',str(correct),' Total: ',str(total),' Precision is ',str((correct/total)*100)

print 
print

confusion_matrix(label_actual,label_pred,['a.1','a.2','a.3','a.4','a.24','a.29','a.39','a.45','a.60','a.118','b.6','b.29','b.36','b.40','b.42','b.60','b.82','b.121','c.2','c.3','c.14','c.108','d.3','d.79','d.92','d.129','e.3','f.23','g.39'])



#unique.keys()[i]+ ' ' + unique.values()[i]+ '\n')



