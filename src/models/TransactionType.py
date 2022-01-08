from enum import Enum

class TransactionType(Enum):
    DAILY = 0
    SEND = 1
    RECEIVE = 2
    BET = 3
    HOURLY = 4