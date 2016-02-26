import pickle
import math
import copy

FOLDER = './b.1.1_supfam/'
TEST_FNAME ='b.1.1_test'
FAM_NAMES = ['b.1.1.0','b.1.1.1','b.1.1.2','b.1.1.3','b.1.1.4']


DLG_stored = []
freq = dict()
corpus = ''
test = ''
X = 0

def load_data(family,test):
	global freq,corpus,X

	fname = FOLDER+family+'.txt'
	f = open(fname,'r');
	data =  f.readline();
	data+= test
	f.close();
	n = 1
	ngrams_dict = dict()
	for j in range(len(data) - n + 1):
        	temp = data[j:j + n]
		if temp in ngrams_dict:
			ngrams_dict[temp] +=1
		else:
			ngrams_dict[temp] =1

	freq = copy.deepcopy(ngrams_dict)
	corpus = copy.deepcopy(data)
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
		       		fam = words[1]
				continue
			else:
				test.append([fam,text])
				text = ''
				words = line.split(' ')
        			fam = words[1]
		
		else:
			text+=line.strip()


	test.append([fam,text])
	#print test
	return test



test_list = process_test(TEST_FNAME)
print len(test_list)

correct = 0
total = 0

for item in test_list:
	test_case = item[0]
	test = item[1]
	max_compression = -1000
	label = []
	total +=1
	for family in FAM_NAMES:
		
		load_data(family,test)
		
		#print 'len of corpus ',family,' ',str(X)

		DL = corpusDL()
		#print 'DL is ',str(DL)

		output,compression = OpSeg(test)
		#print output
		with open( FOLDER+'OUTPUTS/'+family+'_output.txt','w') as f:
		    for i in range(len(output)):
			#f.write("[")
		        f.write(output[i]+ ', ')
			#f.write("] ")
		print 'family ',str(family),'  compression ',str(compression)
		if compression > max_compression:
			max_compression = compression
			label = family
		
	
		DLG_stored = []
		freq = {}
	
	print '\nPredicted : '+str(label)+'	Actual : '+test_case
	print  test_case == label
	if test_case == label:
		correct+=1.0

print 'Precision is ',str((correct/total)*100)





#unique.keys()[i]+ ' ' + unique.values()[i]+ '\n')



