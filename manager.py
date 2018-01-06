from multiprocessing import Process, Queue

class Manager( object ):

	def __init__( self, total_procs ):
		self.total = total_procs
		self.counter = 0
		self.init()


	def init():
		self.proc_list = [ None ] * self.total


def Slave( Process ):

	def __init__( self, dataset ):
		self.dataset = dataset

			
