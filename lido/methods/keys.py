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


def find_duplicated_keys(
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
            duplicates.append((keys_dict[key["key"]], key))

    return duplicates


def _get_withdrawal_credentials(chain_id: int):
    """
    @param chain_id: Network chain id
    @return: Possible withdrawal credentials
    """
    return [bytes.fromhex(cred[2:]) for cred in WITHDRAWAL_CREDENTIALS[chain_id]]


def validate_keys(w3: Web3, keys: List[OperatorKey], strict=False) -> List[OperatorKey]:
    """
    @param w3: Web3
    @param keys: List of keys to validate
    @param strict: Should be used for new keys. It will check that key was signed using contract's actual WC
    @return: List of keys that are invalid
    """
    actual_credentials = LidoContract.getWithdrawalCredentials(w3)[""]
    withdrawal_credentials = [actual_credentials]

    if not strict:
        withdrawal_credentials.extend(_get_withdrawal_credentials(w3.eth.chain_id))

    deposit_domain = compute_deposit_domain(GENESIS_FORK_VERSION[w3.eth.chain_id])

    invalid_keys = []

    for key in keys:
        for withdrawal_credential in withdrawal_credentials:
            is_valid = validate_key(key, withdrawal_credential, deposit_domain)
            if is_valid:
                break
        else:
            invalid_keys.append(key)

    return invalid_keys


def validate_key(
    key: OperatorKey, withdrawal_credential: bytes, deposit_domain: bytes
) -> bool:
    """
    @param key: Key to check.
    @param withdrawal_credential: Possible credential.
    @param deposit_domain: Magic bytes.
    @return: Bool - Valid or Invalid this key
    """
    g1_pub_key = G1Element.from_bytes(key["key"])
    g2_signature = G2Element.from_bytes(key["depositSignature"])

    ETH32 = 32 * 10 ** 9
    deposit_message = DepositMessage(
        pubkey=key["key"],
        withdrawal_credentials=withdrawal_credential,
        amount=ETH32,
    )

    message = compute_signing_root(deposit_message, deposit_domain)
    is_valid = PopSchemeMPL.verify(g1_pub_key, message, g2_signature)

    if is_valid:
        return is_valid

    return False
