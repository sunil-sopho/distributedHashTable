import sys
import hashlib 
from config import *

def gethash(str):
	return hashlib.sha256(str.encode()).hexdigest()[:Logsize] 


class Node(object):

	def __init__(self,nodeId):
		self.nodeId = nodeId
		self.inuse = True
		self.loging = False

	def getSuccessor(self):
		return


	def getPredecessor(self):
		return

	def findSuccessor(self,id):
		return

	def findPredecessor(self,id):
		return


	def closestPrecedingFinger(self,id):
		return

	def ping(self):
		return

	def join(self,node):
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
	 print(gethash("sunil"))