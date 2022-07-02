from abc import ABC, abstractmethod


class JYBase(ABC):

    @abstractmethod
    def get_globals(self):
        return None
