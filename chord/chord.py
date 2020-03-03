import sys
import hashlib 
from config import *
import numpy as np
debugMode = 0

def gethash(strn):
	strn = str(strn)
	var = Logsize%4
	if var >0:
		var = 1
	return hashlib.sha256(strn.encode()).hexdigest()[:int(Logsize/4)+var] 


class Chord(object):
	def __init__(self):
		self.initNode = None
		self.ar = []


	def lookup(self,key):
		node = self.ar[np.random.randint(0,len(self.ar))]
		# node = self.initNode
		return node.get(key,int(gethash(key),16),0)
	def add(self,key,data):
		node = self.ar[np.random.randint(0,len(self.ar))]
		node.put(key,data,int(gethash(key),16))


	def addNode(self,node):
		node.join(self.initNode)
		if self.initNode is None:
			self.initNode = node
		self.ar.append(node)
		return 




class fingerRow(object):
	def __init__(self,n,i):
		self.start = (n+pow(2,i))%size
		self.end = (n+pow(2,i+1)-1)%size
		self.node = None
	def getnode(self):
		return self.node

def inbetween(c,a,b):
	if a < b:
		return a< c and c<=b
		## @sunil check for a<=c
	return a <c or c<=b

def inbetween2(c,a,b):
	if a < b:
		return a <= c and c<b
		## @sunil check for a<=c
	return a <=c or c<b

def inbetween1(c,a,b):
	if a < b:
		return a< c and c<b
	return a < c or c<b

class Node(object):

	def __init__(self,nodeId):
		if nodeId is None:
			print("Node Id entered is None")
			sys.exit(-1)
		self.nodeId = nodeId
		self.hashid = gethash(self.nodeId)
		self.n = int(gethash(self.nodeId),16)
		self.inuse = True
		self.loging = False
		self.finger = [fingerRow(self.n,i) for i in range(Logsize)]
		## successor and predecessor vars
		self._successor = self
		self._predecessor = None
		self._dict = {}


	def debug(self):
		if debugMode > 2:
			print()
			print(self.n," : ",self._successor.n," : ",self._predecessor.n)
			for i in range(Logsize):
				print(i+1," : ",self.finger[i].start," : ",self.finger[i].getnode().n)
			print()
	

	def getSuccessor(self):

		return

	def getPredecessor(self):
		return

	def successor(self):
		return self._successor

	def predecessor(self):
		return self._predecessor

	def closestPrecedingNode(self,id):
		if debugMode > 3:
			print("jump here for preceding node:",self.n," : ",id)
		for i in range(Logsize):
			if debugMode > 2:
				print("check ",self.finger[Logsize-i-1].node.n," : ",self.n," : ",id)
			if inbetween1(self.finger[Logsize-i-1].node.n,self.n,id):
				# print("hit here : ",self.finger[Logsize-i-1].node.n)
				return self.finger[Logsize-i-1].node
		return self

	def findSuccessor(self,id):
		# if id == self.n:
		# 	return self
		if inbetween(id,self.n,self._successor.n):
			if debugMode > 2:
				print(id,"=",self.n,"=",self._successor.n)
				self.debug()
			return self._successor

		node = self.closestPrecedingNode(id)
		if node is None:
			print("failed at findSuccessor ")
			sys.exit(1)
		if node is self:
			return self

		return node.findSuccessor(id)

	def findSuccessorGet(self,id):
		if inbetween(id,self.n,self._successor.n):
			if debugMode > 2:
				print(id,"=",self.n,"=",self._successor.n)
				self.debug()
			return self._successor

		node = self.closestPrecedingNode(id)
		if node is None:
			print("failed at findSuccessor ")
			sys.exit(1)
		if node is self:
			return self	

		return node

	def findSuccessorMode(self,id):
		if id == self.n:
			return self
		if id == self._successor.n:
			return self._successor

		if inbetween2(id,self.n,self._successor.n):
			if debugMode > 2:
				print(id,"=",self.n,"=",self._successor.n)
				self.debug()
			return self._successor

		node = self.closestPrecedingNode(id)
		if node is None:
			print("failed at findSuccessor ")
			sys.exit(1)
		if node is self:
			return self

		return node.findSuccessor(id)	


	def findPredecessor(self,id):
		if debugMode > 3:
			print("findPredecessor : ",self.n," : ",id)
		## if alone in ring case
		if self.successor() == self:
			return self

		nodeCopy = self.findSuccessorMode(id)

		if nodeCopy is None:
			print("failed at findPredecessor ")
			sys.exit(1)	
		if nodeCopy.n == id:
			return nodeCopy

		# print(nodeCopy._predecessor.n,"==========")
		return nodeCopy._predecessor


	# def closestPrecedingFinger(self,id):
	# 	print("closestPrecedingFinger :: ",self.n)
	# 	for i in range(Logsize):
	# 		if inbetween1(self.finger[Logsize-i-1].node.n,self.n,id):
	# 			# print("============ ",self.finger[Logsize-i-1].node.n)
	# 			return self.finger[Logsize-i-1].node
	# 	# print("closestPrecedingFinger return self")
	# 	return self

	def ping(self):
		return

	def initFingerTable(self,node):
		if node is None:
			for i in range(Logsize):
				self.finger[i].node = self
			self._successor = self.finger[0].node
			self._predecessor = self
			return
		else:
			self.finger[0].node = node.findSuccessorMode(self.finger[0].start)
			# print("setting succeror :",self.finger[0].node.n," : ",self.finger[0].start)
			self._successor = self.finger[0].node
			self._predecessor = self._successor._predecessor


		for i in range(Logsize-1):
			if debugMode > 3:
				print(i)
				print(self.finger[i+1].start," : ",self.n," == ",self.finger[i].node.n)
			if inbetween(self.finger[i+1].start,self.n,self.finger[i].node.n):
				# print("here ")
				self.finger[i+1].node = self.finger[i].node
			else:
				self.finger[i+1].node = node.findSuccessorMode(self.finger[i+1].start)

		self._successor._predecessor = self
		self._predecessor._successor = self
		return

	def updateOthers(self):
		# print("updateOthers")
		self.debug()
		for i in range(Logsize):
			pred = self.findPredecessor((self.n-int(pow(2,i))+size)%size)
			if pred is not self:
				# print("update ,",pred.n," :: ",self.n," :: ",i)
				pred.updateFingerTable(self,i)
				# pred.debug()
				# self.debug()
				# print("------------------------------------")

		return

	def updateFingerTable(self,node,i):
		if debugMode > 2:
			print(node.n," : ",self.finger[i].start," : ",self.finger[i].node.n,"---",self.predecessor().n)
		if self.finger[i].start == self.finger[i].node.n:
			return
		if inbetween2(node.n,self.finger[i].start,self.finger[i].node.n):
			if debugMode > 2:
				print("updating:",self.n,":",node.n," : ",i+1)
				self.debug()
				self._predecessor.debug()

			self.finger[i].node = node 
			p = self.predecessor()
			p.updateFingerTable(node,i)
		return

	def join(self,node):
		self.initFingerTable(node)
		self.updateOthers()
		return


	def notify(self,node):
		if self._predecessor == None or inbetween(node.n,self._predecessor.n,self.n):
			self._predecessor = node
		return

	def stablize(self):
		x = self._successor._predecessor
		if inbetween1(x.n,self.n,self._successor.n):
			self._successor = x
		self._successor.notify(self)
		return

	def fixFingers(self):
		return

	def shutdown(self):
		self.inuse = False
		return

	def fix_finger(self,node):
		for i in range(Logsize):
			self.finger[i].node = node.findSuccessor(self.finger[i].start)

	def get(self,key,hashid,num):
		# print(num)
		try : 
			# print("is here: ",num," : ",self.n," : ",hashid)
			# print(self._dict)	
			return self._dict[key],num+1
		except Exception as e:	
			# print("is here2: ",num," : ",self.n)

			successor = self.findSuccessorGet(hashid)
			if successor.n == self.n:
				"""
					this node
				"""
				return None,num+1
			else:
				# num +=1
				a,b =  successor.get(key,hashid,num+1)
				return a,b
		

	def put(self,key,data,hashid):
		successor = self.findSuccessor(hashid)
		# if debugMode > 2:

		# print(hashid, " :=: ",self.n," :=: ",successor.n)

		if successor.n == self.n:
			"""
				this node
			"""
			# print(self.n,": : ",hashid)
			self.debug()
			self._dict[key] = data
		else:
			successor.put(key,data,hashid)
		return


if __name__ == "__main__":
	 # prints all available algorithms 
	print(size)
	chord = Chord()
	ar = []
	st = set()
	tr = 0
	for i in range(10):
		node = Node(i+tr)
		while node.n in st:
			tr +=1
			node = Node(i+tr)
		st.add(node.n)
		print("inserting node : ",i+1," : ",node.n)

		chord.addNode(node)
		ar.append(node)
		for x in ar:
			x.debug()
	# 		if len(ar) > 3:
	# 			x.fix_finger(ar[np.random.randint(0,len(ar))])
	# for x in ar:
	# 		x.stablize()
	# 		if len(ar) > 3:
	# 			x.fix_finger(ar[np.random.randint(0,len(ar))])
	# for x in ar:
	# 	x.debug()
	# debugMode = 0
	# print("max val :,",max(ar))
	allentry = []
	allentry2 = []
	szSet =set()
	for i in range(10000):
		var = np.random.randint(0,1000000)
		while var in szSet:
			var = np.random.randint(0,1000000)
		allentry.append(var)
		allentry2.append(int(gethash(var),16))
		chord.add(var,var)

	allhops = []

	for i in range(100000):
		val = allentry[np.random.randint(0,len(allentry))]
		ans,hop = chord.lookup(val)
		# print(hop)
		allhops.append(hop)
		# print(ans, ":: ",val)
		if val != ans:
			print(val,":",ans)
			sys.exit(-1)

	print(max(allhops)," : ",min(allhops))
	# print(allhops)
	print(np.mean(np.array(allhops)))

	# print(allentry2)
	add=0
	for x in ar:
		add+=len(x._dict)
		# print(x.n," = ",len(x._dict),end=" : ")

	print()
	print()
	print(add)