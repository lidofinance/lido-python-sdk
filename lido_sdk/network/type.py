from enum import IntEnum


class Network(IntEnum):
    Mainnet = 1
    Kovan = 42
    Rinkeby = 4
    Görli = 5
    xDai = 100
    Ropsten = 3


# Network
GENESIS_FORK_VERSION = {
    Network.Mainnet: bytes.fromhex("00000000"),
    Network.Görli: bytes.fromhex("00001020"),
    Network.Ropsten: bytes.fromhex("00000000"),
    Network.Rinkeby: bytes.fromhex("00000000"),
}

# Existing withdrawal credentials on the chain
# Will be filtered for unique values
# Will be used as a fallback for used keys
WITHDRAWAL_CREDENTIALS = {
    Network.Mainnet: [
        "0x009690e5d4472c7c0dbdf490425d89862535d2a52fb686333f3a0a9ff5d2125e"
    ],
    Network.Görli: [
        "0x00040517ce98f81070cea20e35610a3ae23a45f0883b0b035afc5717cc2e833e"
    ],
    Network.Ropsten: [
        "0x01000000000000000000000002139137fdd974181a49268d7b0ae888634e5469",
        "0x000000000000000000000000ff139137fdd974181a49268d7b0ae888634e5469",
        "0x000000000000000000000000aa139137fdd974181a49268d7b0ae888634e5469",
        "0x010000000000000000000000aa139137fdd974181a49268d7b0ae888634e5469",
        "0x73c72beecbd832c9ce342e61a772c8cfe6f1c6d661b19a98317b5dac05ce9685",
    ],
    Network.Rinkeby: [],
}
