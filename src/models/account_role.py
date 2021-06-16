"""This module manages the account type enumeration."""
from enum import Enum


class AccountRole(Enum):
    """This class manages the account type enumeration."""
    CLIENT = 1
    CLIENT_EMPLOYEE = 2
    MANAGER = 3
