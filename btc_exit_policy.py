"""Pure exit-policy predicates for BTC paper-trade experiments."""
from __future__ import annotations

import math
from typing import Any


def should_exit_on_trailing_retrace(observed_bid: Any, trailing_floor: Any, *, enabled: bool = True) -> bool:
    """Decide whether a take-profit pullback alone closes a paper position.

    Other exits (fixed stop, chart stop, confirmed reversal, and settlement)
    remain separate and are not disabled by this predicate.
    """
    if not enabled:
        return False
    try:
        bid = float(observed_bid)
        floor = float(trailing_floor)
    except (TypeError, ValueError, OverflowError):
        return False
    if not math.isfinite(bid) or not math.isfinite(floor):
        return False
    return bid <= floor
