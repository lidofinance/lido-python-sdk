"""
Eth2 deposit utilities
https://github.com/ethereum/eth2.0-deposit-cli
"""

from constants.chains import Eth2Chains
from constants.eth2 import FORK_VERSIONS, DOMAIN_DEPOSIT, ZERO_BYTES32
from ssz import Serializable, uint64, bytes4, bytes32, bytes48


def get_fork_version_by_chain(chain: Eth2Chains) -> bytes:
    return FORK_VERSIONS[chain]


class SigningData(Serializable):
    fields = [
        ("object_root", bytes32),
        ("domain", bytes32)
    ]


class ForkData(Serializable):
    fields = [
        ("current_version", bytes4),
        ("genesis_validators_root", bytes32),
    ]


def compute_deposit_domain(fork_version: bytes) -> bytes:
    """
    Deposit-only `compute_domain`
    """
    if len(fork_version) != 4:
        raise ValueError(
            f"Fork version should be in 4 bytes. Got {len(fork_version)}."
        )

    domain_type = DOMAIN_DEPOSIT
    fork_data_root = compute_deposit_fork_data_root(fork_version)
    return domain_type + fork_data_root[:28]


def compute_deposit_fork_data_root(current_version: bytes) -> bytes:
    """
    Return the appropriate ForkData root for a given deposit version.
    """
    genesis_validators_root = ZERO_BYTES32  # For deposit, it's fixed value
    if len(current_version) != 4:
        raise ValueError(
            f"Fork version should be in 4 bytes. Got {len(current_version)}."
        )

    return ForkData(
        current_version=current_version,
        genesis_validators_root=genesis_validators_root,
    ).hash_tree_root


def compute_signing_root(ssz_object: Serializable, domain: bytes) -> bytes:
    """
    Return the signing root of an object by calculating the root of the object-domain tree.
    The root is the hash tree root of:
    https://github.com/ethereum/eth2.0-specs/blob/dev/specs/phase0/beacon-chain.md#signingdata
    """
    if len(domain) != 32:
        raise ValueError(
            f"Domain should be in 32 bytes. Got {len(domain)}."
        )

    return SigningData(
        object_root=ssz_object.hash_tree_root,
        domain=domain,
    ).hash_tree_root


class DepositMessage(Serializable):
    """
    Ref: https://github.com/ethereum/eth2.0-specs/blob/dev/specs/phase0/beacon-chain.md#depositmessage
    """

    fields = [
        ("pubkey", bytes48),
        ("withdrawal_credentials", bytes32),
        ("amount", uint64),
    ]
