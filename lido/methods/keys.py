from typing import List, Tuple

from blspy import PopSchemeMPL, G1Element, G2Element
from lido.eth2deposit.ssz import (
    compute_deposit_domain,
    DepositMessage,
    compute_signing_root,
)
from web3 import Web3

from lido.contract import LidoContract
from lido.methods.typing import OperatorKey
from lido.network.type import WITHDRAWAL_CREDENTIALS, GENESIS_FORK_VERSION


def find_keys_duplicates(
    keys: List[OperatorKey],
) -> List[Tuple[OperatorKey, OperatorKey]]:
    """
    Find all duplicates in list of keys

    @param keys: List of keys
    @return: Returns list of pair keys (key_1, key_2) that are duplicating
    """
    keys_dict = {}
    duplicates = []

    for key in keys:
        if key["key"] not in keys_dict:
            keys_dict[key["key"]] = key
        else:
            duplicates.append((key, keys_dict[key["key"]]))

    return duplicates


def _get_withdrawal_credentials(chain_id: int):
    """
    @param chain_id: Network chain id
    @return: Possible withdrawal credentials
    """
    return [bytes.fromhex(cred[2:]) for cred in WITHDRAWAL_CREDENTIALS[chain_id]]


def validate_keys(w3: Web3, keys: List[OperatorKey]) -> List[OperatorKey]:
    """
    @param w3: Web3
    @param keys: List of keys to validate
    @return: List of keys that are invalid
    """
    actual_credentials = LidoContract.getWithdrawalCredentials(w3)[""]
    withdrawal_credentials = [
        *_get_withdrawal_credentials(w3.eth.chain_id),
        actual_credentials,
    ]

    deposit_domain = compute_deposit_domain(GENESIS_FORK_VERSION[w3.eth.chain_id])

    invalid_keys = []

    for key in keys:
        is_valid = validate_key(key, withdrawal_credentials, deposit_domain)
        if not is_valid:
            invalid_keys.append(key)

    return invalid_keys


def validate_key(
    key: OperatorKey, withdrawal_credentials: List[bytes], deposit_domain: bytes
) -> bool:
    """
    @param key: Key to check.
    @param withdrawal_credentials: List of possible creds.
    @param deposit_domain: Magic bytes.
    @return: Bool - Valid or Invalid this key
    """
    g1_pub_key = G1Element.from_bytes(key["key"])
    g2_signature = G2Element.from_bytes(key["depositSignature"])

    for wc in withdrawal_credentials:
        ETH32 = 32 * 10 ** 9
        deposit_message = DepositMessage(
            pubkey=key["key"],
            withdrawal_credentials=wc,
            amount=ETH32,
        )

        message = compute_signing_root(deposit_message, deposit_domain)
        is_valid = PopSchemeMPL.verify(g1_pub_key, message, g2_signature)

        if is_valid:
            return is_valid

    return False
