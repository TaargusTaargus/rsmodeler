from multiprocessing import Process, Queue
from etl import transform
from utilities import split_dict

class Manager( object ):

	def __init__( self, total_procs ):
		self.total = total_procs
		self.init_parallel()


	def init_parallel( self ):
		self.proc_list = []
		for proc in range( self.total ):
			self.proc_list.append( self.init_proc( proc ) )


	def is_running( self ):
		return sum( [ int( proc.is_alive() ) in self.proc_list ] )


	def run( self ):
		results = []

		for proc in self.proc_list:
			proc.run()

		while self.proc_list:
			proc = self.proc_list.pop( 0 )

			if proc.is_alive():
				self.proc_list.append( proc )
			else:
				results = results + proc.finish()

		return results



class Worker( Process ):

	def __init__( self, procedure, args ):
		self.procedure = procedure
		self.args = args


	def run( self ):
		self.dataset = self.procedure( *self.args )

	def finish( self ):
		return self.dataset



class TransformManager( Manager ):

	def __init__( self, dataset, total_procs ):
		self.dataset = split_dict( dataset, total_procs ) 
		Manager.__init__( self, total_procs )

	def	init_proc( self, proc_number ):
		return Worker( transform, ( self.dataset[ proc_number ], None, None ) )

	def transform( self ):
		self.run()

	
