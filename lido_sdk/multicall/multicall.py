from concurrent.futures import ThreadPoolExecutor

from multicall import Call, Multicall as DefaultMulticall

from lido_sdk import config
from lido_sdk.multicall.multicall_address import MULTICALL_ADDRESSES


class Multicall(DefaultMulticall):
    """
    Upgraded version of Multicall from https://github.com/banteg/multicall.py

    Improves:
        - Added MAX_CALLS_PER_MULTICALL param to avoid huge and slow batches in Multicall
        - results from multicall is not a dict, but a list now. We are making a lot of requests to one contract's method,
        so we don't wanna loose data.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.max_call_bunch = config.MULTICALL_MAX_BUNCH
        self.max_workers = config.MULTICALL_MAX_WORKERS
        self.max_retries = config.MULTICALL_MAX_RETRIES

    def __call__(self):
        calls_list = [
            self.calls[i : i + self.max_call_bunch]
            for i in range(0, len(self.calls), self.max_call_bunch)
        ]

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
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

        for retry_num in range(self.max_retries):
            try:
                block, outputs = aggregate(args)
            except ValueError as error:
                if retry_num == self.max_retries - 1:
                    raise error
            else:
                results = []
                for call, output in zip(self.calls, outputs):
                    results.append(call.decode_output(output))

                return results

        # Not expected exception
        raise Exception("Bug in Multicall")
