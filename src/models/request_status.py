"""This module manages the status of the requests."""
from enum import Enum


class RequestStatus(Enum):
    """This class manages the status of the requests."""
    REQUEST = 1
    ACCEPTED = 2
    REJECTED = 3
    CANCELLED = 4
    FINISHED = 5
