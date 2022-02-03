from abc import ABC, abstractmethod


class BaseNormaliser(ABC):

    @abstractmethod
    def normalise(self, pattern):
        pass
