from web3 import Web3

from lido_sdk.contract import LidoContract


def get_status(w3: Web3):
    return {
        "isStopped": LidoContract.isStopped(w3)[""],
        "totalPooledEther": LidoContract.getTotalPooledEther(w3)[""],
        "withdrawalCredentials": LidoContract.getWithdrawalCredentials(w3)[""],
        "bufferedEther": LidoContract.getBufferedEther(w3)[""],
        **LidoContract.getFee(w3),
        **LidoContract.getFeeDistribution(w3),
        **LidoContract.getBeaconStat(w3),
        "last_block": w3.eth.getBlock("latest")["number"],
        "last_blocktime": w3.eth.getBlock("latest")["timestamp"],
    }
