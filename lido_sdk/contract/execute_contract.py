from typing import List, Dict

from multicall import Call
from web3 import Web3

from lido_sdk.multicall import Multicall


def execute_contract_multicall(
    w3: Web3,
    registry_address: str,
    abi_method_name: str,
    abi_input: List[Dict],
    abi_returns: List[Dict],
    args_list: List[List],
):
    """
    @param w3: Web3 instance
    @param registry_address: Contract address in current network
    @param abi_method_name: Contract name of method
    @param abi_input: Params that this method receives, exp: [{'type': 'uint256', 'name': 'contractId'}, ...]
    @param abi_returns: Params that function returns, exp: [{'type': 'uint256', 'name': 'signedKeys'}, ...]
    @param args_list: List of bunches of arg each of those will be used to call contract, exp: [[True, 1], [True, 2], ...]
    @return: List of results from each call that we did.
    """
    return Multicall(
        calls=[
            _create_contract_call(
                w3, registry_address, abi_method_name, abi_input, abi_returns, args
            )
            for args in args_list
        ],
        _w3=w3,
    )()


def execute_contract_call(
    w3: Web3,
    registry_address: str,
    abi_method_name: str,
    abi_input: List[Dict],
    abi_returns: List[Dict],
    args: List = None,
) -> Dict:
    """
    @param w3: Web3 instance
    @param registry_address: Contract address in current network
    @param abi_method_name: Contract name of method
    @param abi_input: Params that this method receives, exp: [{'type': 'uint256', 'name': 'contractId'}, ...]
    @param abi_returns: Params that function returns, exp: [{'type': 'uint256', 'name': 'signedKeys'}, ...]
    @param args: List of arguments that will be used to call this function
    @return: List of results from each call that we did.
    """
    return _create_contract_call(
        w3, registry_address, abi_method_name, abi_input, abi_returns, args
    )()


def _create_contract_call(
    w3: Web3,
    registry_address: str,
    abi_method_name: str,
    abi_input: List[Dict],
    abi_returns: List[Dict],
    args: List = None,
) -> Call:
    input_args = ",".join([x["type"] for x in abi_input])
    output_args = ",".join([x["type"] for x in abi_returns])
    returns = [(abi_return["name"], lambda y: y) for abi_return in abi_returns]

    function = f"{abi_method_name}({input_args})({output_args})"

    call = Call(
        target=registry_address,
        function=function,
        returns=returns,
        _w3=w3,
    )

    call.args = args

    return call
