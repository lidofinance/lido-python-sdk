from concurrent.futures import ThreadPoolExecutor

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

    MAX_CALLS_PER_MULTICALL = 275
    MAX_WORKERS = 6

    def __call__(self):
        calls_list = [
            self.calls[i : i + self.MAX_CALLS_PER_MULTICALL]
            for i in range(0, len(self.calls), self.MAX_CALLS_PER_MULTICALL)
        ]

        with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
            thread_results = executor.map(self.execute, calls_list)

        result = []

        for thread_result in thread_results:
            result.extend(thread_result)

        return result

    def execute(self, calls):
        aggregate = Call(
            MULTICALL_ADDRESSES[self.w3.eth.chain_id],
            "aggregate((address,bytes)[])(uint256,bytes[])",
            returns=None,
            _w3=self.w3,
            block_id=self.block_id,
        )

        args = [[[call.target, call.data] for call in calls]]
        try:
            block, outputs = aggregate(args)
        except ValueError:
            # It seems it is {'code': -32000, 'message': 'execution aborted (timeout = 5s)'}
            # Try again
            block, outputs = aggregate(args)

        results = []
        for call, output in zip(self.calls, outputs):
            results.append(call.decode_output(output))

        return results
