# iberror.py
# Various error codes

from enum import Enum


class IBError(Enum):
    No_Error = 1
    Invalid_URL = 2
    Request_Timeout = 3


if __name__ == '__main__':
    print("=== iberror.py ===")