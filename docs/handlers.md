# **Handlers** 

## **Database Connection Handler**
The database handler establishes necessary connection with the database based on information provided in the config.ini file.

All errors encountered during the course of connection are logged to logs/d2b.log
```python
class DatabaseConn:
    def __init__(self, connector=env("SERVER", "DB_CONNECTOR")) -> None:
        """Establish database connection based on the server settings in config.ini

        Args:
            log_file (str, optional): The name or path to the file where error will be logged. Defaults to ERROR_LOG path in config.ini
            connection (str, optional): The database connector, Default to DB_CONNECTOR in config.ini
        """
        # Load connection variables from config.ini
        self.DB_HOST = env("SERVER", "DB_HOST")
        self.DB_PORT = env("SERVER", "DB_PORT")
        self.DB_DATABASE = env("SERVER", "DB_DATABASE")
        self.DB_USERNAME = env("SERVER", "DB_USERNAME")
        self.DB_PASSWORD = env("SERVER", "DB_PASSWORD")
        self.connector = connector

    def __alchemy(self):
        return create_engine(
            f"postgresql+psycopg2://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_DATABASE}"
        )

    def __pg(self):
        # Establish a connection with the db
        try:
            conn = pg.connect(
                host=self.DB_HOST,
                dbname=self.DB_DATABASE,
                user=self.DB_USERNAME,
                password=self.DB_PASSWORD,
                port=self.DB_PORT,
            )
            return conn
        except Exception as e:
            print(e)

    def connect(self):
        conn = None
        if self.connector.lower() == "alchemy":
            conn = self.__alchemy()
        elif self.connector.lower() == "pg":
            conn = self.__pg()
        else:
            raise TypeError("Invalid connector, expects either pg or alchemy")
        return conn
```

## **Env Connection Handler**

```python
# scripts/handlers/env_handler.py

# read configuraton file
config_file = "../d2b/config.ini"
config = ConfigParser()
config.read(config_file)


def env(section, key, value=None):
    """
    Sets or returns config file section, key value

    parameters
    ----------
    section: The config file section
    key: A key in the selected section
    value: desired value for the selected key, if not set, returns the key's
    current value.
    """
    if value is None:
        return config[section][key]
    else:
        config[section][key] = value
        return config

```

## **Service Handler**
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

The log handler control how logs are formatted.
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