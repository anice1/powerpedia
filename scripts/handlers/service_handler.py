from abc import ABC, abstractclassmethod


class Service(ABC):
    @abstractclassmethod
    def execute_service(self, *args, **kwargs):
        return None
