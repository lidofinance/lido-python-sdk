from dataclasses import dataclass


@dataclass
class Operator:
    index: int
    active: bool
    name: str
    rewardAddress: str
    stakingLimit: int
    stoppedValidators: int
    totalSigningKeys: int
    usedSigningKeys: int


@dataclass
class OperatorKey:
    index: int
    key: bytes
    depositSignature: bytes
    used: bool
