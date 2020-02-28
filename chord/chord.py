import sys
import hashlib 
from config import *

def gethash(strn):
	strn = str(strn)
	return hashlib.sha256(strn.encode()).hexdigest()[:Logsize//4] 


class Chord(object):
	def __init__(self):
		self.initNode = None

	def addNode(self,node):
		node.join(self.initNode)
		if sel.finitNode is None:
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
		return a<= c and c<b
	return a <=c or c<b

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
		self.successor = -1
		self.predecessor = -1


	def debug(self):
		for i in range(Logsize):
			print(i+1," : ",self.finger[i].start," : ",self.finger[i].getnode())
		print()
		print(self.n)
	

	def getSuccessor(self):

		return

	def getPredecessor(self):
		return

	def successor(self,id):

		return

	def findSuccessor(self,id):
		node = findPredecessor(id)
		if node is None:
			print("failed at findSuccessor ")
			sys.exit(1)

			## @sunil check if id needed here
		return	node.successor()

	def findPredecessor(self,id):
		nodeCopy = self
		while not inbetween(id,nodeCopy.n,nodeCopy.successor().n):
			nodeCopy = nodeCopy.closestPrecedingFinger(id)
		if nodeCopy is None:
			print("failed at findPredecessor ")
			sys.exit(1)	
		return nodeCopy


	def closestPrecedingFinger(self,id):
		for i in range(Logsize):
			if inbetween(self.finger[Logsize-i-1].node,n,id):
				return self.finger[Logsize-i-1].node
		print("closestPrecedingFinger return self")
		return self

	def ping(self):
		return

	def initFingerTable(self,node):
		if node is None:
			for i in range(Logsize):
				self.finger[i].node = self
			return

		self.finger[0].node = node.findSuccessor(finger[0].start)
		successorNode = finger[0].node
		predecessorNode = successorNode.predecessor

		successorNode.predecessor = self
		predecessorNode.successor = self

		for i in range(Logsize-1):
			if inbetween(self.finger[i+1].start,self.n,self.finger[i].node):
				self.finger[i+1].node = self.finger[i].node
			else:
				self.finger[i+1].node = node.findSuccessor(finger[i+1].start)

		return

	def updateOthers(self):
		for i in range(Logsize):
			pred = self.findPredecessor(self.n-int(pow(2,i)))
			pred.updateFingerTable(self,i)

		return

	def updateFingerTable(self,node,i):
		if inbetween(node.n,self.n,self.finger[i].node.n):
			self.finger[i].node = node 
			p = self.predecessor()
			p.updateFingerTable(node,i)
		return

	def join(self,node):
		self.initFingerTable(node)
		self.updateOthers()
		return


	def notify(self,node):
		return

	def stablize(self):

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
	for i in range(100):
		print("inserting node : ",i+1)
		node = Node(i)
		chord.addNode(node)
