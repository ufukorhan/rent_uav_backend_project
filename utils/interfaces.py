from abc import ABC, abstractmethod


from abc import ABC, abstractmethod

class Service(ABC):
    """
    Abstract base class for defining a service interface.

    Subclasses must implement the following methods:
    - create_object(*args, **kwargs)
    - update_object(*args, **kwargs)
    - delete_object(*args, **kwargs)
    """
    @abstractmethod
    def create_object(self, *args, **kwargs):
        ...

    @abstractmethod
    def update_object(self, *args, **kwargs):
        ...

    @abstractmethod
    def delete_object(self, *args, **kwargs):
        ...
