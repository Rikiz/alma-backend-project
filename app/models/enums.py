from enum import Enum


class LeadState(str, Enum):
    PENDING = "PENDING"
    REACHED_OUT = "REACHED_OUT"
