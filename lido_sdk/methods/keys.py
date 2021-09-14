from concurrent.futures import ProcessPoolExecutor
from typing import List, Tuple

from lido_sdk.eth2deposit.ssz import (
    compute_deposit_domain,
    DepositMessage,
    compute_signing_root,
)
from web3 import Web3

from lido_sdk.contract import LidoContract
from lido_sdk.methods.typing import OperatorKey
from lido_sdk.network.type import WITHDRAWAL_CREDENTIALS, GENESIS_FORK_VERSION
from lido_sdk.blstverify.verifier import verify


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


def validate_keys(w3: Web3, keys: List[OperatorKey]) -> List[OperatorKey]:
    """
    @param w3: Web3
    @param keys: List of keys to validate
    @return: List of keys that are invalid
    """
    deposit_domain = compute_deposit_domain(GENESIS_FORK_VERSION[w3.eth.chain_id])

    actual_credential = LidoContract.getWithdrawalCredentials(w3)[""]
    possible_credentials = _get_withdrawal_credentials(w3.eth.chain_id)

    invalid_keys = []

    key_params = [
        (key, actual_credential, possible_credentials, deposit_domain) for key in keys
    ]

    with ProcessPoolExecutor() as executor:
        for key, is_valid in zip(
            keys, executor.map(_executor_validate_key, key_params)
        ):
            if not is_valid:
                invalid_keys.append(key)

    return invalid_keys


def _executor_validate_key(data: Tuple):
    key, actual_credential, possible_credential, deposit_domain = data

    is_valid = validate_key(key, actual_credential, deposit_domain)

    if not is_valid and key.get("used", False):
        for wc in possible_credential:
            is_valid = validate_key(key, wc, deposit_domain)

            if is_valid:
                break

    return is_valid


def validate_key(
    key: OperatorKey, withdrawal_credential: bytes, deposit_domain: bytes
) -> bool:
    """
    @param key: Key to check.
    @param withdrawal_credential: Possible credential.
    @param deposit_domain: Magic bytes.
    @return: Bool - Valid or Invalid this key
    """
    pub_key = key["key"]
    signature = key["depositSignature"]

    ETH32 = 32 * 10 ** 9
    deposit_message = DepositMessage(
        pubkey=key["key"],
        withdrawal_credentials=withdrawal_credential,
        amount=ETH32,
    )

    message = compute_signing_root(deposit_message, deposit_domain)
    is_valid = verify(pub_key, message, signature)

    if is_valid:
        return is_valid

    return False
