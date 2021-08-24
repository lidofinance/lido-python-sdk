from multicall.constants import Network


# Existing withdrawal credentials on the chain
# Will be filtered for unique values
# Will be used as a fallback for used keys or in strict mode when validating signatures
WITHDRAWAL_CREDENTIALS = {
    Network.Mainnet: [
        "0x009690e5d4472c7c0dbdf490425d89862535d2a52fb686333f3a0a9ff5d2125e"
    ],
    Network.Görli: [
        "0x00040517ce98f81070cea20e35610a3ae23a45f0883b0b035afc5717cc2e833e"
    ],
}
