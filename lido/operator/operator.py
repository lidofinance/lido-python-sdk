import typing as t
import logging

from multicall import Call, Multicall

logger = logging.getLogger(__name__)


def get_operators_data(
    w3,
    registry_address: str,
    registry_abi_path: str,
) -> t.List[t.Dict]:
    """Fetch information for each node operator

    Example output:
    [{
        'id': 0,
        'active': True,
        'name': 'Staking Facilities',
        'rewardAddress': '0xdd4bc51496dc93a0c47008e820e0d80745476f22',
        'stakingLimit': 2040,
        'stoppedValidators': 0,
        'totalSigningKeys': 2500,
        'usedSigningKeys': 2000
    }...]
    """

    operators_n = Call(w3, registry_address, "getNodeOperatorsCount()(uint256)")()
    logger.debug(f"{operators_n=}")
    if operators_n == 0:
        logger.warning(f"no operators")  # fixme assert if not test env
        return []
    assert operators_n < 1_000_000, "too big operators_n"

    calls = Multicall(
        w3,
        [
            Call(
                w3,
                registry_address,
                [
                    "getNodeOperator(uint256,bool)(bool,string,address,uint64,uint64,uint64,uint64)",
                    i,
                    True,
                ],
                [[i, None]],
            )
            for i in range(operators_n)
        ],
    )()

    calls_list = list(calls.values())

    # Adding index as first data of operator
    calls_with_indeces = [[i] + list(item) for i, item in enumerate(calls_list)]

    # Getting function data from contract ABI
    function_abi = next(
        x
        for x in get_contract(w3, address=registry_address, path=registry_abi_path).abi
        if x["name"] == "getNodeOperator"
    )

    # Adding "id" and the rest of output name keys
    op_keys = ["id"] + [x["name"] for x in function_abi["outputs"]]
    operators = [dict(zip(op_keys, op)) for op in calls_with_indeces]

    return operators
