"""Settlement payout math for the BTC binary-contract dashboard.

This reports deterministic contract mechanics only. It does not estimate the
probability of an outcome or the probability of an early exit filling.
"""
from __future__ import annotations

import math
from typing import Any


def _finite_number(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return number if math.isfinite(number) else None


def calculate_settlement_economics(
    entry_ask_cents: Any,
    max_trade_dollars: Any,
    fee_cents_per_contract: Any = 2.0,
) -> dict[str, Any]:
    """Return a max-budget binary-contract settlement estimate, or a reason unavailable.

    The estimated contract count is rounded down to whole contracts and uses
    the configured entry fee. It does not include early-exit fees or slippage.
    """
    ask = _finite_number(entry_ask_cents)
    budget = _finite_number(max_trade_dollars)
    fee = _finite_number(fee_cents_per_contract)
    if ask is None or not 0 < ask < 100:
        return {"available": False, "reason": "A valid entry ask between 0¢ and 100¢ is required."}
    if budget is None or budget <= 0:
        return {"available": False, "reason": "A positive per-trade budget is required."}
    if fee is None or fee < 0:
        return {"available": False, "reason": "The configured entry fee is invalid."}

    cost_per_contract = ask + fee
    if cost_per_contract >= 100:
        return {"available": False, "reason": "Entry price plus fee leaves no positive settlement profit."}
    budget_cents = budget * 100
    contracts = max(0, int(math.floor((budget_cents + 1e-9) / cost_per_contract)))
    if contracts < 1:
        return {
            "available": False,
            "reason": "The trade budget does not cover one contract plus its configured entry fee.",
            "entry_ask_cents": round(ask, 4),
            "fee_cents_per_contract": round(fee, 4),
            "max_trade_budget_dollars": round(budget, 4),
        }

    entry_cost = contracts * cost_per_contract
    payout = contracts * 100.0
    return {
        "available": True,
        "contracts": contracts,
        "entry_ask_cents": round(ask, 4),
        "fee_cents_per_contract": round(fee, 4),
        "max_trade_budget_dollars": round(budget, 4),
        "estimated_entry_cost_cents": round(entry_cost, 4),
        "gross_payout_if_correct_cents": round(payout, 4),
        "net_profit_if_correct_cents": round(payout - entry_cost, 4),
        "max_loss_if_wrong_cents": round(entry_cost, 4),
        "break_even_probability_percent": round(entry_cost / payout * 100, 4),
        "settlement_only": True,
        "note": "At settlement, a correct standard binary contract pays $1 and an incorrect one pays $0. Amounts include configured entry fees; early exits, slippage, and actual fill prices can differ.",
    }
