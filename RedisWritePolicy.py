from enum import Enum 

class RedisWritePolicy(Enum):
    WRITEBACK = 1
    WRITETHROUGH = 2