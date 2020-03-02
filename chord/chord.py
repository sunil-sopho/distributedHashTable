import sys
import hashlib 
from config import *

debugMode = 0

def gethash(strn):
	strn = str(strn)
	return hashlib.sha256(strn.encode()).hexdigest()[:Logsize//4] 


class Chord(object):
	def __init__(self):
		self.initNode = None

	def addNode(self,node):
		node.join(self.initNode)
		if self.initNode is None:
			self.initNode = node
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


	def debug(self):
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
		print("jump here for preceding node:",self.n," : ",id)
		for i in range(Logsize):
			# print("check ",self.finger[Logsize-i-1].node.n," : ",self.n," : ",id)
			if inbetween1(self.finger[Logsize-i-1].node.n,self.n,id):
				# print("hit here : ",self.finger[Logsize-i-1].node.n)
				return self.finger[Logsize-i-1].node
		return self

	def findSuccessor(self,id):
		if inbetween(id,self.n,self._successor.n):
			return self._successor

		node = self.closestPrecedingNode(id)
		if node is None:
			print("failed at findSuccessor ")
			sys.exit(1)
		if node is self:
			return self

		return node.findSuccessor(id)


	def findPredecessor(self,id):
		print("findPredecessor : ",self.n," : ",id)
		## if alone in ring case
		if self.successor() == self:
			return self

		nodeCopy = self.findSuccessor(id)

		if nodeCopy is None:
			print("failed at findPredecessor ")
			sys.exit(1)	


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
			self.finger[0].node = node.findSuccessor(self.finger[0].start)
			print("setting succeror :",self.finger[0].node.n," : ",self.finger[0].start)
			self._successor = self.finger[0].node
			self._predecessor = self._successor._predecessor

			print(self._predecessor.n)
			print(self._successor.n)

		for i in range(Logsize-1):
			# print(i)
			# print(self.finger[i+1].start," : ",self.n," == ",self.finger[i].node.n)
			if inbetween(self.finger[i+1].start,self.n,self.finger[i].node.n):
				# print("here ")
				self.finger[i+1].node = self.finger[i].node
			else:
				self.finger[i+1].node = node.findSuccessor(self.finger[i+1].start)

		self._successor._predecessor = self
		self._predecessor._successor = self
		return

	def updateOthers(self):
		print("updateOthers")

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
		print(node.n," : ",self.n," : ",self.finger[i].node.n,"---",self.predecessor().n)
		if inbetween(node.n,self.n,self.finger[i].node.n):
			print("updating:",self.n,":",node.n)
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



if __name__ == "__main__":
	 # prints all available algorithms 
	print(size)
	chord = Chord()
	ar = []
	st = set()
	tr = 0
	for i in range(100):
		print()
		print()
		print()
		node = Node(i+tr)
		while node.n in st:
			tr +=1
			node = Node(i+tr)
		st.add(node.n)
		print("inserting node : ",i+1," : ",node.n)

		chord.addNode(node)
		ar.append(node)

		# for x in ar:
		# 	x.stablize()
		# 	x.debug()
