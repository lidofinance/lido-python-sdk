from typing import List, Optional, Tuple, Dict

from web3 import Web3

from lido_sdk import config
from lido_sdk.methods import (
    find_duplicated_keys,
    validate_keys,
    get_operators_indexes,
    get_operators_data,
    get_operators_keys,
    get_status,
)
from lido_sdk.methods.typing import Operator, OperatorKey
from lido_sdk.network import Network


class LidoException(Exception):
    pass


class Lido:
    operators_indexes = None
    operators = None
    keys = None

    def __init__(self, w3: Web3, **kwargs):
        self._w3 = w3
        self._set_configs(kwargs)

        if self._w3.eth.chain_id == Network.Görli:
            from web3.middleware import geth_poa_middleware

            # Checking by value b/c we don't know the key
            if geth_poa_middleware not in self._w3.middleware_onion:
                raise LidoException(
                    "PoA middleware isn't injected into Web3 middleware onion"
                )

    def _set_configs(self, kwargs: Dict):
        chain_id = self._w3.eth.chain_id
        # Lifehack to cache chain_id
        self._w3.eth._chain_id = lambda: chain_id

        for key, value in kwargs.items():
            setattr(config, key, value)

    def get_operators_indexes(self) -> List[int]:
        """
        @return: List of operator's indexes in Lido.
        """
        self.operators_indexes = get_operators_indexes(self._w3)
        return self.operators_indexes

    def get_operators_data(
        self, operators_indexes: Optional[List[int]] = None
    ) -> List[Operator]:
        """
        It will fetch details for each operator specified.

        @param operators_indexes: List operators indexes to fetch.
        @return: List of operators details.
        """
        operators_indexes = (
            self.operators_indexes if operators_indexes is None else operators_indexes
        )
        if operators_indexes is None:
            raise LidoException(
                "`get_operators_indexes` should be called first or provide `operators_indexes` param"
            )

        self.operators = get_operators_data(self._w3, operators_indexes)

        return self.operators

    def get_operators_keys(
        self, operators: Optional[List[Operator]] = None
    ) -> List[OperatorKey]:
        """
        Returns all keys for specified operators.

        @param operators: List of operators details. We need few fields to fetch "index" and "totalSigningKeys".
        @return: List of keys. Each key can be identified and refetched by "index" and "operator_index".
        """
        operators = self.operators if operators is None else operators
        if operators is None:
            raise LidoException(
                "`get_operators_data` should be called first or provide `operators` param"
            )

        self.keys = get_operators_keys(self._w3, operators)

        return self.keys

    def validate_keys(
        self, keys: Optional[List[OperatorKey]] = None
    ) -> List[OperatorKey]:
        """
        Validate all provided keys with pub_key, signature, withdrawal_credentials and DepositDomain.

        @param keys: List of operators keys.
        @return: All invalid keys that were found.
        """
        keys = self.keys if keys is None else keys
        if keys is None:
            raise LidoException(
                "`get_operators_keys` should be called first or provide `keys` param"
            )

        return validate_keys(self._w3, keys)

    def find_duplicated_keys(
        self, keys: Optional[List[OperatorKey]] = None
    ) -> List[Tuple[OperatorKey, OperatorKey]]:
        """
        Find and returns all keys duplicates.

        @param keys: List a keys to check.
        @return: List of duplicate pairs keys.
        """
        keys = self.keys if keys is None else keys
        if keys is None:
            raise LidoException(
                "`get_operators_keys` should be called first or provide `keys` param"
            )

        return find_duplicated_keys(keys)

    def get_status(self) -> dict:
        """
        Return a dict with Lido contract actual state.
        """
        return get_status(self._w3)

    def fetch_all_keys_and_validate(self) -> Dict[str, list]:
        """
        Function that makes all flow: fetches operators and keys, than it validate all keys.

        @return: Is a dict with two keys.
        - invalid_keys - for details see Lido.validate_keys method.
        - duplicated_keys - for details see Lido.find_duplicated_keys method.
        """
        self.get_operators_indexes()
        self.get_operators_data()
        self.get_operators_keys()
        invalid_keys = self.validate_keys()
        duplicated_keys = self.find_duplicated_keys()

        return {
            "invalid_keys": invalid_keys,
            "duplicated_keys": duplicated_keys,
        }
