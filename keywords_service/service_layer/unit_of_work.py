import abc

from keywords_service.adapters import repository 

class AbstractUnitOfWork(abc.ABC):
	collection: repository.AbstractCollectionRepository

	def __exit__(self, *args):
		self.rollback()

	@abc.abstractmethod
	def commit(self):
		raise NotImplementedError

	@abc.abstractmethod
	def rollback(self):
		raise NotImplementedError
	


#  class AbstractAuthenticatedUnitOfWork