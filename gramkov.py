# -*- coding: UTF-8-*-

"""
gramkov.py
A markov chain text generator that knows his grammar.
"""

import nltk
import random
import json
from sys import stdout

from markov20 import *
from util import *

class Gramkov():
	def __init__(self):
		self.corp = ""
		self.struct = []
		self.posdict = {}
		self.m20 = None

	# loads the corpus
	def loadcorp(self,corp):
		self.corp = list((corp).replace("  ","").replace("\n\n"," ").replace("\r\n"," ").replace("\n"," ").replace("\r"," ")
		.replace("=","").replace("--"," -- ").replace(" '"," ' ").replace("' "," ' ").replace("*","").replace("  "," ")[:].lower())
		for i in range(0,len(self.corp)):
			if ord(self.corp[i]) >= 128:
				self.corp[i] = "#"
		self.corp = "".join(self.corp)
		self.tokens = nltk.word_tokenize(self.corp)
		self.tagged = nltk.pos_tag(self.tokens)

	# extract sentence structure from corpus
	def makestruct(self):
		for i in range(0,len(self.tagged)):
			self.struct.append(self.tagged[i][1])

	# extract part of speech information of the words from corpus
	def makeposdict(self):
		for i in range(0,len(self.tagged)):
			if self.tagged[i][1] not in self.posdict.keys():
				self.posdict[self.tagged[i][1]] = {}

			if self.tagged[i][0] not in self.posdict[self.tagged[i][1]]:
				self.posdict[self.tagged[i][1]][self.tagged[i][0]] = 0

			self.posdict[self.tagged[i][1]][self.tagged[i][0]] += 1

	# build a markov chain from the corpus
	def makemarkov(self):
		self.m20 = Markov20(self.corp)

	# saves and loads data
	def fIO(self,name,op="save",data="struct"):
		if op == "save":
			if data == "struct":
				f1 = open("train/"+name+".stt.json","w")
				f1.write(json.dumps(self.struct))
			if data == "posdict":
				f1 = open("train/"+name+".pdt.json","w")
				f1.write(json.dumps(self.posdict))
			if data == "markov":
				f1 = open("train/"+name+".mrk.json","w")
				f1.write(json.dumps(self.m20.corp))
		if op == "load":
			if data == "struct":
				path = "train/"+name+".stt.json"
				f1 = open(path,"r")
				self.struct = json.loads(f1.read())
				print "struct loaded: "+path
			if data == "posdict":
				path = "train/"+name+".pdt.json"
				f1 = open(path,"r")
				self.posdict = json.loads(f1.read())
				print "posdict loaded: "+path
			if data == "markov":
				path = "train/"+name+".mrk.json"
				f1 = open(path,"r")
				self.m20 = Markov20("")
				self.m20.corp = json.loads(f1.read())
				print "markov chain loaded: "+path
		if f1: f1.close()

	# set up everything for generation
	def prepare(self):
		self.makestruct()
		self.makeposdict()
		self.makemarkov()

	# get a random / specific sentence structure
	def getsent(self,n=-1):
		if n== -1:
			return random.choice("@".join(self.struct).split(".@")).split("@")[:-1]+["."]
		return "@".join(self.struct).split(".@")[n].split("@")[:-1]+["."]

	# generate using backtracking
	def gen(self,sentstruct,debug=False):
		output = [""] * len(sentstruct)
		backtrack = [0] * len(sentstruct)

		# can't find an appropriate word; making do
		def emergency(ind):
			try:
				return random.choice(self.posdict[sentstruct[ind]].keys())
			except:
				return "thing"

		# put all candidate words into a pool for selection
		# the higher-scored a candidates is, the more copies of it exist in the pool
		# score = PoS score x (Markov score + weight)
		def pool(ind):
			candpool = {}

			for p in self.posdict[sentstruct[ind]].keys():
				candpool[p] = [self.posdict[sentstruct[ind]][p],0]

			if ind > 0:
				for i in range(1,3):
					for p in self.m20.candidates(output[max(0,ind-i):ind]):
						if p not in candpool.keys():
							candpool[p] = [0,0]
						candpool[p][1] += 1
			else:
				for p in candpool.keys():
					candpool[p][1] = 1

			candscores = dict()
			candscores["ERR"]=0
			for p in candpool.keys():
				sco = candpool[p][0]*candpool[p][1]
				if sco > 0:
					candscores[p] = sco
			candscores = sorted(candscores.items(), key=lambda x:x[1],reverse=True)

			choosepool = []
			for c in candscores:
				choosepool += [c]*(c[1]  +50)
			random.shuffle(choosepool)

			return choosepool

		# recursive backtracking to fill in all the words
		def solve(ind):
			if (ind == len(sentstruct)):
				if (debug): print
				return output
			else:
				backtrack[ind]+=1
				if backtrack[ind] > 100:
					output[ind] = emergency(ind)
					return solve(ind+1)

				if debug:
					# stdout.write("\r["+"".join([str(i) for i in backtrack])+"]")
					stdout.write("\r"+str(ind+1)+"/"+str(len(sentstruct)))
					stdout.flush()

				choosepool = pool(ind)
				for c in choosepool:
					if c[1] != 0:

						output[ind] = c[0]
						solution = solve(ind+1)
						if (solution != None):
							return solution
						output[ind] = c[0]
				return None
		return solve(0)

	# generate one sentence
	def genSentence(self,ind=-1,debug=False):
		out = ""
		while out == "":
			output = self.gen(self.getsent(ind),debug)
			if output != None:
				out += "\n"+" ".join(output).replace('``','"').replace("''",'"').replace(" ,",
					",").replace(" .",".").replace(" ?","?").replace(" !","!").replace(" ;",";").replace(" :",
					":").replace(" '","'").replace("( ","(").replace(" )",")")

		return sentcase(out)


def run():
	gk = Gramkov()
	# gk.loadcorp(open("corpus/nietzsche.txt").read())
	# gk.prepare()

	# gk.fIO("grammarbook","save","struct")
	# gk.fIO("grammarbook","save","posdict")
	# gk.fIO("grammarbook","save","markov")

	gk.fIO("grammarbook","load","struct")
	gk.fIO("nietzsche","load","posdict")
	gk.fIO("nietzsche","load","markov")

	print
	for i in range(0,5):
		print gk.genSentence(-1,True)


if __name__ == "__main__":
	print
	run()
	print
