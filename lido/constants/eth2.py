
from typing import Dict
from chains import Eth2Chains


ZERO_BYTES32 = b"\x00" * 32

"""
Eth2-spec constants taken from 
https://github.com/ethereum/eth2.0-specs/blob/dev/specs/phase0/beacon-chain.md
"""
DOMAIN_DEPOSIT = bytes.fromhex("03000000")


FORK_VERSIONS: Dict[Eth2Chains, bytes] = {
    Eth2Chains.MAINNET: bytes.fromhex("00000000"),
    Eth2Chains.PYRMONT: bytes.fromhex("00002009"),
    Eth2Chains.PRATER: bytes.fromhex("00001020")
}
