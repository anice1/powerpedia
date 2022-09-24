# Handlers 

## Database Connection Handler
```python
class DatabaseConn(LogHandler):
    def __init__(self, log_file=env("LOG", "ERROR_LOG")) -> None:
        """Establish database connection based on the server settings in config.ini

        Args:
            log_file (str, optional): the name or path to the file where error will be logged. Defaults to ERROR_LOG path in config.ini
        """
        super().__init__(log_file=log_file)

        self.conn = None
        # Load connection variables from config.ini
        self.DB_HOST = env("SERVER", "DB_HOST")
        self.DB_PORT = env("SERVER", "DB_PORT")
        self.DB_DATABASE = env("SERVER", "DB_DATABASE")
        self.DB_USERNAME = env("SERVER", "DB_USERNAME")
        self.DB_PASSWORD = env("SERVER", "DB_PASSWORD")

    def connect(self):
        # Establish a connection with the db
        try:
            self.conn = pg.connect(
                host=self.DB_HOST,
                dbname=self.DB_DATABASE,
                user=self.DB_USERNAME,
                password=self.DB_PASSWORD,
                port=self.DB_PORT,
            )

        except Exception as e:
            # log error to file
            self.logger.debug(e)
            self.error()

        # self.logger.info(self.conn)
        return self.conn
```

## Env Connection Handler

```python
# read configuraton file
config_file = "../Data2bot-Assessment/config.ini"
config = ConfigParser()
config.read(config_file)


def env(section, key, value=None):
    """
    Sets or returns config file section, key value

    parameters
    ----------
    section: The config file section
    key: A key in the selected section
    value: desired value for the selected key, if not set, returns the key's current value
    """
    if value is None:
        return config[section][key]
    else:
        config[section][key] = value
        return config
```

## Service Handler
```python

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
```

## Log Handler
```python
from Handlers.env_handler import env


class LogHandler:
    def __init__(self, log_file=env("LOG", "ERROR_LOG")):
        # set our database logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(env("LOG", "LOG_LEVEL"))

        # set the log formatter
        self.formatter = logging.Formatter(
            "------------------------\n%(asctime)s \n------------------------\n %(filename)s:  \n \
            \n %(message)s \n  @ %(funcName)s: %(pathname)s"
        )
        # set the file handler
        self.file_handler = logging.FileHandler(filename=log_file)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
```