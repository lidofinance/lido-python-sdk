import json
import os

from lido_sdk.contract.contract import Contract
from lido_sdk.network import Network


LIDO_ADDRESSES = {
    Network.Mainnet: "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84",
    Network.Görli: "0x1643E812aE58766192Cf7D2Cf9567dF2C37e9B7F",
    Network.Ropsten: "0xd40EefCFaB888C9159a61221def03bF77773FC19",
    Network.Rinkeby: "0xF4242f9d78DB7218Ad72Ee3aE14469DBDE8731eD",
    Network.Kintsugi: "0x3a6a994AC0CC96b6DDbaA99F10769384Fa14227B",
    Network.Kiln: "0x3E50180cf438e185ec52Ade55855718584541476",
}

NODE_OPS_ADDRESSES = {
    Network.Mainnet: "0x55032650b14df07b85bF18A3a3eC8E0Af2e028d5",
    Network.Görli: "0x9D4AF1Ee19Dad8857db3a45B0374c81c8A1C6320",
    Network.Ropsten: "0x32c6f34F3920E8c0074241619c02be2fB722a68d",
    Network.Rinkeby: "0x776dFe7Ec5D74526Aa65898B7d77FCfdf15ffBe6",
    Network.Kintsugi: "0xeb7D01f713F59EFfB350D05b7AF66720373D4F41",
    Network.Kiln: "0xb849C5b35DC45277Bad5c6F2c6C77183d842367c",
}


def _get_contract_abi(contract_name: str):
    script_dir = os.path.dirname(__file__)

    with open(os.path.join(script_dir, "abi", contract_name)) as file:
        return json.load(file)


# Load all supported contracts here
LidoContract = Contract(LIDO_ADDRESSES, _get_contract_abi("Lido.json"))
NodeOpsContract = Contract(
    NODE_OPS_ADDRESSES, _get_contract_abi("NodeOperatorsRegistry.json")
)
