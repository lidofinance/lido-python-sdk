from multicall import Call, Multicall as DefaultMulticall

from lido.network.address import MULTICALL_ADDRESSES


class Multicall(DefaultMulticall):
    def __call__(self):
        """Overwrite call to use our MULTICALL_ADDRESSES"""
        aggregate = Call(
            MULTICALL_ADDRESSES[self.w3.eth.chainId],
            'aggregate((address,bytes)[])(uint256,bytes[])',
            returns=None,
            _w3=self.w3,
            block_id=self.block_id
        )
        args = [[[call.target, call.data] for call in self.calls]]
        block, outputs = aggregate(args)
        result = {}
        for call, output in zip(self.calls, outputs):
            result.update(call.decode_output(output))
        return result
