from typing import List

from mev_inspect.schemas.classified_traces import (
    ClassifiedTrace,
    DecodedCallTrace,
    Classification,
)

from mev_inspect.schemas.liquidations import Liquidation


def find_liquidations_from_traces(
    traces: List[ClassifiedTrace],
) -> List[Liquidation]:

    """Inspect list of classified traces and identify liquidation"""

    liquidations: List[ClassifiedTrace] = []
    seen_transactions: List[str] = []
    result: List[Liquidation] = []

    for trace in traces:

        if isinstance(trace, DecodedCallTrace):

            # Check for liquidation and register trace and unique liquidator
            if (
                trace.classification == Classification.liquidate
                and trace.transaction_hash not in seen_transactions
            ):

                liquidations.append(trace)

                result.append(
                    Liquidation(
                        liquidated_user=trace.inputs["_user"],
                        collateral_address=trace.inputs["_collateral"],
                        collateral_amount=trace.inputs["_purchaseAmount"],
                        reserve=trace.inputs["_reserve"],
                    )
                )

    return result
