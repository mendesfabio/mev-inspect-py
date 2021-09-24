from typing import List, Optional, Dict


from mev_inspect.schemas.classified_traces import (
    ClassifiedTrace,
    DecodedCallTrace,
    Classification,
    Protocol,
)

from mev_inspect.schemas.liquidations import Liquidation

AAVE_CONTRACT_ADDRESSES: List[str] = [
    # AAVE Proxy
    "0x398ec7346dcd622edc5ae82352f02be94c62d119",
    # AAVE V2
    "0x7d2768de32b0b80b7a3454c06bdac94a69ddc7a9",
    # AAVE V1
    "0x3dfd23a6c5e8bbcfc9581d2e864a68feb6a076d3",
    # AAVE V2 WETH
    "0x030ba81f1c18d280636f32af80b9aad02cf0854e",
]


def is_transfer_to_liquidator(
    trace: ClassifiedTrace, liquidator: str
) -> Optional[ClassifiedTrace]:
    """Check if transfer is to liquidator"""

    if isinstance(trace, DecodedCallTrace):
        try:
            if (
                trace.inputs["recipient"] == liquidator
                and trace.from_address in AAVE_CONTRACT_ADDRESSES
            ):
                return trace

        except KeyError:
            pass
        try:
            if (
                trace.inputs["dst"] == liquidator
                and trace.from_address in AAVE_CONTRACT_ADDRESSES
            ):
                return trace
        except KeyError:
            return None

    return None


def get_liquidations(
    traces: List[ClassifiedTrace],
) -> List[Liquidation]:

    """Inspect list of classified traces and identify liquidation"""
    # liquidation_traces: List[DecodedCallTrace] = []
    liquidations: List[Liquidation] = []
    transfers_to: Dict = {}
    unique_transaction_hashes: List = []

    for trace in traces:

        if (
            trace.classification == Classification.liquidate
            and isinstance(trace, DecodedCallTrace)
            and trace.transaction_hash not in unique_transaction_hashes
        ):

            liquidator = trace.from_address

            for t in traces:

                to_result = is_transfer_to_liquidator(t, liquidator)
                if to_result and not (
                    to_result.transaction_hash in transfers_to.keys()
                ):
                    transfers_to[trace.transaction_hash] = to_result

            unique_transaction_hashes.append(trace.transaction_hash)
            try:
                received_amount = int(
                    transfers_to[trace.transaction_hash].inputs["amount"]
                )
            except KeyError:
                received_amount = int(
                    transfers_to[trace.transaction_hash].inputs["wad"]
                )

            liquidations.append(
                Liquidation(
                    liquidated_user=trace.inputs["_user"],
                    collateral_token_address=trace.inputs["_collateral"],
                    debt_token_address=trace.inputs["_reserve"],
                    liquidator_user=liquidator,
                    debt_purchase_amount=trace.inputs["_purchaseAmount"],
                    protocol=Protocol.aave,
                    received_amount=received_amount,
                    # aToken lookup is out of scope for now, WIP
                    received_token_address=trace.inputs["_collateral"],
                    transaction_hash=trace.transaction_hash,
                    block_number=trace.block_number,
                )
            )

    print("\n")
    print(transfers_to)
    print("\n")
    print(liquidations)
    return liquidations
