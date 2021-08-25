from multicall import Call, Multicall as DefaultMulticall

from lido.multicall.multicall_address import MULTICALL_ADDRESSES


class Multicall(DefaultMulticall):
    """
    Upgraded version of Multicall from https://github.com/banteg/multicall.py

    Improves:
        - Added MAX_CALLS_PER_MULTICALL param to avoid huge and slow batches in Multicall
        - results from multicall is not a dict, but a list now. We are making a lot of requests to one contract's method,
        so we don't wanna loose data.
    """
    MAX_CALLS_PER_MULTICALL = 300

    def __call__(self):
        aggregate = Call(
            MULTICALL_ADDRESSES[self.w3.eth.chainId],
            "aggregate((address,bytes)[])(uint256,bytes[])",
            returns=None,
            _w3=self.w3,
            block_id=self.block_id,
        )

        result = []
        calls_list = [
            self.calls[i:i + self.MAX_CALLS_PER_MULTICALL]
            for i in range(0, len(self.calls), self.MAX_CALLS_PER_MULTICALL)
        ]

        for calls in calls_list:
            args = [[[call.target, call.data] for call in calls]]
            block, outputs = aggregate(args)

            for call, output in zip(self.calls, outputs):
                result.append(call.decode_output(output))

        return result
