import redis
import json
import os

from mech.mania.starter_pack.domain.memory.set_value_result import SetValueResult


class MemoryObject:
    DEFAULT_STRING = ""
    DEFAULT_FLOAT = 0.0
    DEFAULT_INT = 0
    DEFAULT_BOOLEAN = False

    DEFAULTS = {
        bool: DEFAULT_BOOLEAN,
        int: DEFAULT_INT,
        float: DEFAULT_FLOAT, 
        str: DEFAULT_STRING
    }

    TARGET_ENGINE = ''
    TEAM_NAME = ''
    PASSWORD = ''
    HOST = ''
    PORT = ''

    USER_DATA_KEY = ''

    REDIS_CONNECTION = None
    user_data = {}

    def __init__(self, target_engine = None, team_name = None, host = None, port = None, password = None):
        self.TARGET_ENGINE = target_engine if target_engine else os.getenv("TARGET_ENGINE")
        self.TEAM_NAME = team_name if team_name else os.getenv("TEAM_NAME")
        self.HOST = host if host else os.getenv("REDIS_HOST")
        self.PORT = port if port else int(os.getenv("REDIS_PORT"))
        self.PASSWORD = password if password else os.getenv("REDIS_PASSWORD")
        
        self.USER_DATA_KEY = f'{self.TEAM_NAME.lower().replace(" ", "_")}_{self.TARGET_ENGINE}'

        self.initialize()

    def set_value(self, key, value):
        if not self.is_connected():
            self.initialize()

        if not self.is_connected():
            return SetValueResult.REDIS_NOT_CONNECTED

        if not self.is_valid_value(value):
            return SetValueResult.INVALID_OBJECT_TYPE

        self.user_data[key] = value

        self.save_data()

        return SetValueResult.OPERATION_SUCCESS

    def get_value(self, key, data_type):
        if data_type not in self.DEFAULTS:
            return (None, False)

        if key not in self.user_data:            
            return (self.DEFAULTS[data_type], False)

        value = self.user_data[key]
        return (value, isinstance(value, data_type))

    def remove_key(self, key):
        if key not in self.user_data:
            return False

        value = self.user_data[key]

        del self.user_data[key]

        return True

    def is_valid_value(self, value):
        return type(value) in self.DEFAULTS

    def initialize(self):
        self.get_connection()
        user_data_status = self.fetch_data()

    def is_connected(self):
        return bool(self.REDIS_CONNECTION)

    def save_data(self):
        if not self.is_connected():
            return False

        self.REDIS_CONNECTION.set(self.USER_DATA_KEY, json.dumps(self.user_data))

        return True

    def close_connection(self):
        if not self.is_connected():
            return False

        self.REDIS_CONNECTION.close()

        return True

    def save_and_close(self):
        if not self.save_data():
            return False

        return self.close_connection()

    def fetch_data(self):
        if not self.is_connected():
            self.get_connection()

        if not self.is_connected():
            self.user_data = {}
            return False

        redis_connection = self.REDIS_CONNECTION

        data = redis_connection.get(self.USER_DATA_KEY)

        if not data:
            self.user_data = {}
            return False

        data = data.decode('utf-8')
        data = json.loads(data)
        self.user_data = data

        return True

    def get_connection(self):
        try:
            connection = redis.Redis(host=self.HOST, port=self.PORT, socket_connect_timeout=1, password=self.PASSWORD)

            ping = connection.ping()

            if ping:
                self.REDIS_CONNECTION = connection
                return True

            self.REDIS_CONNECTION = None
            return False
        except Exception:
            self.REDIS_CONNECTION = None
            return False