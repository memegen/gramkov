import random
class Markov20():
	def __init__(self,corp,delim=" ",punc=[".",",",";","?","!",'"',"'","(",")"]):
		self.corp = corp
		self.punc = punc
		self.delim = delim
		for p in self.punc: self.corp = self.corp.replace(p,delim+p)
		self.corp = self.corp.split(delim)
	def predict(self,wl):
		return random.choice([self.corp[i+len(wl)] for i in range(0,len(self.corp)-len(wl)) if self.corp[i:i+len(wl)] == wl ])
	def candidates(self,wl):
		return [self.corp[i+len(wl)] for i in range(0,len(self.corp)-len(wl)) if self.corp[i:i+len(wl)] == wl ]
	def sentence(self,w,d,l=0):
		res = w + self.delim
		i = 0
		while (l != 0 and i < l) or (l==0 and w != self.punc[0]):
			#print res.split(self.delim)[-1-d:-1]
			w = self.predict(res.split(self.delim)[-1-d:-1])
			res += w + self.delim
			i+=1
		for p in self.punc: res = res.replace(self.delim+p,p)
		return res
	def randsentstart(self):
		return random.choice(self.delim.join(self.corp).split(self.punc[0]+self.delim)).split(self.delim)[0]


if __name__ == "__main__":
	f1 = open("corpus/nietzsche.txt") #s3.amazonaws.com/text-datasets/nietzsche.txt	
	corp = (f1.read()).replace("  ","").replace("\n"," ").replace("\r\n"," ").replace("\r"," ").replace("=","")
	m20 = Markov20(corp)
	for i in range(0,3):
		print m20.sentence(m20.randsentstart(),2)
