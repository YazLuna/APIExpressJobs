"""This module manages the status of the services."""
from enum import Enum


class ServiceStatus(Enum):
    """This class manages the status of the services."""
    ACTIVE = 1
    INACTIVE = 2
    BLOCKED_UP = 3
