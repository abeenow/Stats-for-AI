import glob
import math

class NBClassify:
	
	def __init__(self):
		
		# Extract the featues in to key value pairs
		self.label_dict = {}
		self.mean = {}
		self.stdev = {}
		self.label_prob = {}
		self.actual_data={}
		self.predicted_data = {}
		self.accuracy = 0
		self.train_data = 0
		self.test_data = 0
					
	def generateTrainData(self,train_file):
		
		fp = open(train_file)
		for line in fp:
			if(line.startswith('@') == False):
				tmp = []
				self.train_data = self.train_data + 1
				for val in line.split(','):
					tmp.append(val)
					key = tmp[-1].rstrip('\n')
					val = [float(fval) for fval in tmp[:-1]]
				if(self.label_dict.has_key(key) == True):
					self.label_dict[key].append(val)
				else: 
					self.label_dict[key] = []
					self.label_dict[key].append(val)
		self.populateMeanVar()
							
	def populateMeanVar(self):
		
		# Get the mean, variance dictionaries here
		for key in self.label_dict:
			self.label_prob[key] = float(len(self.label_dict[key])) / float(self.train_data) 
			self.mean[key] = [calcMean(item) for item in zip(*self.label_dict[key])]
			self.stdev[key] = [calcVar(item) for item in zip(*self.label_dict[key])]
	
	def Classify(self,test_file):
		# Parse the file into required vectors
		fp = open(test_file)
		line_no = 0
		for line in fp:
			if(line.startswith('@') == False):
				line_no = line_no + 1
				tmp = []
				for val in line.split(','):
					tmp.append(val)
				val = [float(fval) for fval in tmp[:-1]]
				self.predicted_data[line_no] = self.calcProbability(val)
				self.actual_data[line_no] = tmp[-1].rstrip('\n')
		self.test_data = line_no		
				
	def guassProb(self,x,label,mean,stdev):
		prob = 0.01
		if ( x == 0 and stdev == 0 and mean == 0):
			prob = 1
		if ( stdev != 0.0 ):
			exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
			prob = (1 / (math.sqrt(2*math.pi) * stdev)) * exponent
		return 	(prob)

	def calcProbability(self,dataset):
		ret_list = {}
		for key in self.label_prob:
			# Has all the possible lables along with its probability
			prob = self.label_prob[key]
			for ind in range(1,len(dataset)):
				scale = self.guassProb(dataset[ind],key,self.mean[key][ind],self.stdev[key][ind])
				prob = prob * scale
			ret_list[key] = prob
		return 	ret_list
		
	def getMaximumProb(self,linedict,lineno,fp):
		max_val = 0
		reqd_key = ''
		symbol=u'\u2714'
		for ind in linedict:
			if(linedict[ind] > max_val ):
				max_val = linedict[ind]
				reqd_key = ind
		if(reqd_key != self.actual_data[lineno]):
			symbol=u'\u274C'
		fp.write(("\t\t"+str(lineno)+"\t\t"+ reqd_key+"\t\t"+self.actual_data[lineno]+"\t\t"+symbol+"\n").encode('utf8'))
		if(reqd_key == self.actual_data[lineno]):
			self.accuracy = self.accuracy + 1
			
def calcMean(tup):
	return sum(tup)/float(len(tup))
 
def calcVar(tup):
	avg = calcMean(tup)
	variance = sum([pow(x-avg,2) for x in tup])/float(len(tup)-1)
	return math.sqrt(variance)
		
def main():
	for folder in glob.glob('Data/*/*'):
		print('Strating to compute: '+folder)
		nbc = NBClassify()
		f=open(folder+'/result.dat','w')
		nbc.generateTrainData(folder+'/train.arff')
		nbc.Classify(folder+'/test.arff')
		f.write("\n\tLine Number\t\tPredicted value\t\tActual value\t\tMatch\n")
		for key1 in nbc.predicted_data:
			nbc.getMaximumProb(nbc.predicted_data[key1],key1,f)
		f.write("\nCorrect predictions= "+str(nbc.accuracy))
		f.write("\nTotal data= "+str(nbc.test_data))
		f.write("\nAccuracy of classification: {0:.2f}%".format(100 * float(nbc.accuracy)/float(nbc.test_data)))
		print('Successfully generated result at: '+folder+'/result.dat')
	return 0

if __name__ == '__main__':
	main()
