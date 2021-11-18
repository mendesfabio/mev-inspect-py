from typing import Optional, List
from mev_inspect.schemas.transfers import Transfer
from mev_inspect.schemas.swaps import Swap
from mev_inspect.schemas.traces import (
    DecodedCallTrace,
    Protocol,
)
from mev_inspect.schemas.classifiers import (
    ClassifierSpec,
    SwapClassifier,
)


class ZeroExSwapClassifier(SwapClassifier):
    @staticmethod
    def parse_swap(
        trace: DecodedCallTrace,
        prior_transfers: List[Transfer],
        child_transfers: List[Transfer],
    ) -> Optional[Swap]:

        token_in_amount: int = 0
        taker_address: str

        order: List = trace.inputs["order"]

        if "taker" in trace.inputs:
            taker_address = trace.inputs["taker"]
        else:
            taker_address = order[5]

        token_in_address: str = order[0]
        token_out_address: str = order[1]

        token_out_amount: int = trace.inputs["takerTokenFillAmount"]

        pool_address = trace.to_address

        for transfer in child_transfers:
            if transfer.to_address == taker_address:
                token_in_amount = transfer.amount

        return Swap(
            abi_name=trace.abi_name,
            transaction_hash=trace.transaction_hash,
            block_number=trace.block_number,
            trace_address=trace.trace_address,
            pool_address=pool_address,
            protocol=trace.protocol,
            from_address=trace.from_address,
            to_address=trace.to_address,
            token_in_address=token_in_address,
            token_in_amount=token_in_amount,
            token_out_address=token_out_address,
            token_out_amount=token_out_amount,
            error=trace.error,
        )


ZEROX_CONTRACT_SPECS = [
    ClassifierSpec(
        abi_name="exchangeProxy",
        protocol=Protocol.zero_ex,
        valid_contract_addresses=["0xDef1C0ded9bec7F1a1670819833240f027b25EfF"],
    ),
    ClassifierSpec(
        abi_name="exchangeProxyAllowanceTarget",
        protocol=Protocol.zero_ex,
        valid_contract_addresses=["0xf740b67da229f2f10bcbd38a7979992fcc71b8eb"],
    ),
    ClassifierSpec(
        abi_name="exchangeProxyFlashWallet",
        protocol=Protocol.zero_ex,
        valid_contract_addresses=["0x22f9dcf4647084d6c31b2765f6910cd85c178c18"],
    ),
    ClassifierSpec(
        abi_name="exchangeProxyGovernor",
        protocol=Protocol.zero_ex,
        valid_contract_addresses=["0x618f9c67ce7bf1a50afa1e7e0238422601b0ff6e"],
    ),
    ClassifierSpec(
        abi_name="exchangeProxyLiquidityProviderSandbox",
        protocol=Protocol.zero_ex,
        valid_contract_addresses=["0x407b4128e9ecad8769b2332312a9f655cb9f5f3a"],
    ),
    ClassifierSpec(
        abi_name="exchangeProxyTransformerDeployer",
        protocol=Protocol.zero_ex,
        valid_contract_addresses=["0x39dce47a67ad34344eab877eae3ef1fa2a1d50bb"],
    ),
    ClassifierSpec(
        abi_name="wethTransformer",
        protocol=Protocol.zero_ex,
        valid_contract_addresses=["0xb2bc06a4efb20fc6553a69dbfa49b7be938034a7"],
    ),
    ClassifierSpec(
        abi_name="payTakerTransformer",
        protocol=Protocol.zero_ex,
        valid_contract_addresses=["0x4638a7ebe75b911b995d0ec73a81e4f85f41f24e"],
    ),
    ClassifierSpec(
        abi_name="fillQuoteTransformer",
        protocol=Protocol.zero_ex,
        valid_contract_addresses=["0x5ce5174d7442061135ea849970ffc7763920e0fd"],
    ),
    ClassifierSpec(
        abi_name="affiliateFeeTransformer",
        protocol=Protocol.zero_ex,
        valid_contract_addresses=["0xda6d9fc5998f550a094585cf9171f0e8ee3ac59f"],
    ),
    ClassifierSpec(
        abi_name="staking",
        protocol=Protocol.zero_ex,
        valid_contract_addresses=["0x2a17c35ff147b32f13f19f2e311446eeb02503f3"],
    ),
    ClassifierSpec(
        abi_name="stakingProxy",
        protocol=Protocol.zero_ex,
        valid_contract_addresses=["0xa26e80e7dea86279c6d778d702cc413e6cffa777"],
    ),
    ClassifierSpec(
        abi_name="zrxToken",
        protocol=Protocol.zero_ex,
        valid_contract_addresses=["0xe41d2489571d322189246dafa5ebde1f4699f498"],
    ),
    ClassifierSpec(
        abi_name="zrxVault",
        protocol=Protocol.zero_ex,
        valid_contract_addresses=["0xba7f8b5fb1b19c1211c5d49550fcd149177a5eaf"],
    ),
    ClassifierSpec(
        abi_name="devUtils",
        protocol=Protocol.zero_ex,
        valid_contract_addresses=["0x74134cf88b21383713e096a5ecf59e297dc7f547"],
    ),
    ClassifierSpec(
        abi_name="etherToken",
        protocol=Protocol.zero_ex,
        valid_contract_addresses=["0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"],
    ),
    ClassifierSpec(
        abi_name="erc20BridgeSampler",
        protocol=Protocol.zero_ex,
        valid_contract_addresses=["0xd8c38704c9937ea3312de29f824b4ad3450a5e61"],
    ),
]

ZEROX_GENERIC_SPECS = [
    ClassifierSpec(
        abi_name="IBatchFillNativeOrdersFeature",
        protocol=Protocol.zero_ex,
    ),
    ClassifierSpec(
        abi_name="IFeature",
        protocol=Protocol.zero_ex,
    ),
    ClassifierSpec(
        abi_name="IFundRecoveryFeature",
        protocol=Protocol.zero_ex,
    ),
    ClassifierSpec(
        abi_name="ILiquidityProviderFeature",
        protocol=Protocol.zero_ex,
    ),
    ClassifierSpec(
        abi_name="IMetaTransactionsFeature",
        protocol=Protocol.zero_ex,
    ),
    ClassifierSpec(
        abi_name="IMultiplexFeature",
        protocol=Protocol.zero_ex,
    ),
    ClassifierSpec(
        abi_name="INativeOrdersFeature",
        protocol=Protocol.zero_ex,
        classifiers={
            "fillOrKillLimitOrder((address,address,uint128,uint128,uint128,address,address,address,address,bytes32,uint64,uint256),(uint8,uint8,bytes32,bytes32),uint128)": ZeroExSwapClassifier,
            "fillRfqOrder((address,address,uint128,uint128,address,address,address,bytes32,uint64,uint256),(uint8,uint8,bytes32,bytes32),uint128)": ZeroExSwapClassifier,
        },
    ),
    ClassifierSpec(
        abi_name="IOtcOrdersFeature",
        protocol=Protocol.zero_ex,
    ),
    ClassifierSpec(
        abi_name="IOwnableFeature",
        protocol=Protocol.zero_ex,
    ),
    ClassifierSpec(
        abi_name="IPancakeSwapFeature",
        protocol=Protocol.zero_ex,
    ),
    ClassifierSpec(
        abi_name="ISimpleFunctionRegistryFeature",
        protocol=Protocol.zero_ex,
    ),
    ClassifierSpec(
        abi_name="ITestSimpleFunctionRegistryFeature",
        protocol=Protocol.zero_ex,
    ),
    ClassifierSpec(
        abi_name="ITokenSpenderFeature",
        protocol=Protocol.zero_ex,
    ),
    ClassifierSpec(
        abi_name="ITransformERC20Feature",
        protocol=Protocol.zero_ex,
    ),
    ClassifierSpec(
        abi_name="IUniswapFeature",
        protocol=Protocol.zero_ex,
    ),
    ClassifierSpec(
        abi_name="IUniswapV3Feature",
        protocol=Protocol.zero_ex,
    ),
    ClassifierSpec(
        abi_name="IBootstrapFeature",
        protocol=Protocol.zero_ex,
    ),
]

ZEROX_CLASSIFIER_SPECS = ZEROX_CONTRACT_SPECS + ZEROX_GENERIC_SPECS
