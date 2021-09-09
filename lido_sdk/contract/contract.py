from typing import Dict, List, Optional

from web3 import Web3


class Contract:
    """
    Contract class that converts abi interface and list of registry addresses to useful object.
    This is some kind of simplified interfaces from brownie.

    When you receive the Contract instance you will be able to use all contract methods in simple and multicall way.
    Example:
        LidoContract.{contractMethodName}(web3, args)
        or for multicall
        LidoContract.{contractMethodName}_multicall(web3, [args0, args1, ...])
        it is similar to
        LidoContract.{contractMethodName}(web3, args0)
        LidoContract.{contractMethodName}(web3, args1)
        ...
    """

    def __init__(self, registry_addresses: Dict[int, str], contract_abi: List[Dict]):
        """
        @param registry_addresses: It is a dictionary where chain_id is a key and str is the address in this Chain
        where contract is deployed.
        @param contract_abi: Typical contract interface

        Example of usage can be found in lido/contract/load_contract.py
        """
        self.registry_addresses = registry_addresses
        self.contract_abi = contract_abi

        for abi_element in contract_abi:
            if abi_element["type"] == "function":
                self._create_contract_method(abi_element)

    def _create_contract_method(self, abi_function):
        """Create all methods announced in contract's abi"""

        def call(w3: Web3, args: Optional[List] = None):
            from lido_sdk.contract.execute_contract import execute_contract_call

            return execute_contract_call(
                w3,
                self.registry_addresses[w3.eth.chain_id],
                abi_function["name"],
                abi_function["inputs"],
                abi_function["outputs"],
                args=args,
            )

        def multicall(w3: Web3, args_list: Optional[List[List]] = None):
            from lido_sdk.contract.execute_contract import execute_contract_multicall

            args_list = args_list or [[]]

            return execute_contract_multicall(
                w3,
                self.registry_addresses[w3.eth.chain_id],
                abi_function["name"],
                abi_function["inputs"],
                abi_function["outputs"],
                args_list=args_list,
            )

        setattr(self, abi_function["name"], call)
        setattr(self, f"{abi_function['name']}_multicall", multicall)
