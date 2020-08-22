from enum import Enum 

class SetValueResult(Enum):
    OPERATION_SUCCESS = 1
    REDIS_NOT_CONNECTED = 2
    INVALID_OBJECT_TYPE = 3