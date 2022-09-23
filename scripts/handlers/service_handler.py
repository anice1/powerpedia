from abc import ABC, abstractclassmethod


class Service(ABC):

    service_list = None
    service_path = None

    def __init_subclass__(cls, **kwargs) -> None:
        for required in ("service_list", "service_path"):
            if not getattr(cls, required):
                raise TypeError(
                    f"Can't instantiate class {cls.__name__} without {required} attribute defined"
                )
        return super().__init_subclass__(**kwargs)

    @abstractclassmethod
    def services(self, *args, **kwargs):
        return ["".join([self.service_path, service]) for service in self.service_list]

    @abstractclassmethod
    def execute_service(self, *args, **kwargs):
        return None
