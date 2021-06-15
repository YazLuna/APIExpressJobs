"""This module manages the account status enumeration."""
from enum import Enum


class AccountStatus(Enum):
    """This class manages the account status enumeration."""
    ACTIVE = 1
    INACTIVE = 2
    BLOCKED_UP = 3
