from enum import Enum


class RequestStatus(Enum):
    REQUEST = 1
    ACCEPTED = 2
    REJECTED = 3
    CANCELLED = 4
    FINISHED = 5
