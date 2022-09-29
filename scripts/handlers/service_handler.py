from abc import ABC, abstractclassmethod


class Service(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractclassmethod
    def execute_service(self, *args, **kwargs):
        return None
