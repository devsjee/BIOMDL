import pickle
import math
import copy

FNAME = 'PS01199_867'

f = open('./'+FNAME+'/'+FNAME+'.txt','r');
text =  f.readline();
#text = text.replace('_','');
f.close();

X = len(text)
print X

DLG_stored = []
freq = dict()
f = open('./'+FNAME+'/'+FNAME.split('_')[0]+'_ngram_1','rb')
freq = pickle.load(f)
f.close()


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

def OpSeg(U):
	global text
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
			if occurrences(text,ngram)<2:
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
				print 'OS[{}] is now assigned {}'.format(k,OS[k])
				DLG_stored[k] = copy.deepcopy(dlgain)
			elif (dlgain> DLG_stored[k]) and j==0:
				OS[k][:]=[]
				OS[k].append(ngram)
				DLG_stored[k] = copy.deepcopy(dlgain)
		                print 'OS[{}] is now assigned {}'.format(k,OS[k])

	           		 
	return OS[n-1]


def DLG(s):
	global freq,text,X

	suffix = len(s)
	cs = occurrences(text,s)
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

DLG_stored = []
DL = corpusDL()
print DL

test =text
#test="MVKIVTVKTKAYPDQKPGTSGLRKRVKVFQSSTNYAENFIQSIISTVEPAQRQEATLVVGGDGRFYMKEAIQLIVRIAAANGIGRLVIGQNGILSTPAVSCIIRKIKAIGGIILTASHNPGGPNGDFGIKFNISNGGPAPEAITDKIFQISKTIEEYAICPDLKVDLGVLGKQQFDLENKFKPFTVEIVDSVEAYATMLRNIFDFNALKELLSGPNRLKIRIDAMHGVVGPYVKKILCEELGAPANSAVNCVPLEDFGGHHPDPNLTYAADLVETMKSGEHDFGAAFDGDGDRNMILGKHGFFVNPSDSVAVIAANIFSIPYFQQTGVRGFARSMPTSGALDRVANATKIALYETPTGWKFFGNLMDASKLSLCGEESFGTGSDHIREKDGLWAVLAWLSILATRKQSVEDILKDHWHKFGRNFFTRYDYEEVEAEGATKMMKDLEALMFDRSFVGKQFSANDKVYTVEKADNFEYHDPVDGSVSKNQGLRLIFADGSRIIFRLSGTGSAGATIRLYIDSYEKDNAKINQDPQVMLAPLISIALKVSQLQERTGRTAPTVIT" 

output = OpSeg(test)
print output
with open('./'+FNAME+'/output.txt','w') as f:
    for i in range(len(output)):
	#f.write("[")
        f.write(output[i]+ ', ')
	#f.write("] ")

unique = {}
for i in range(len(output)):
    count = unique.get(output[i],0)+1
    unique[output[i]] = count

with open('./'+FNAME+'/output2.txt','w') as f:
    for i in range(len(unique)):
        f.write(str(unique.keys()[i]) + '\t' +str(unique.values()[i])+ '\n')


#unique.keys()[i]+ ' ' + unique.values()[i]+ '\n')



