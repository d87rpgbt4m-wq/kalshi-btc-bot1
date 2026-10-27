import unittest

from btc_trade_economics import calculate_settlement_economics


class SettlementEconomicsTests(unittest.TestCase):
    def test_eighty_cent_contract_reports_payout_profit_loss_and_break_even(self):
        result = calculate_settlement_economics(80, 1.00, 2)
        self.assertTrue(result["available"])
        self.assertEqual(result["contracts"], 1)
        self.assertEqual(result["estimated_entry_cost_cents"], 82)
        self.assertEqual(result["gross_payout_if_correct_cents"], 100)
        self.assertEqual(result["net_profit_if_correct_cents"], 18)
        self.assertEqual(result["max_loss_if_wrong_cents"], 82)
        self.assertEqual(result["break_even_probability_percent"], 82)

    def test_budget_uses_whole_contracts_and_never_exceeds_cap(self):
        result = calculate_settlement_economics(20, 1.00, 2)
        self.assertEqual(result["contracts"], 4)
        self.assertEqual(result["estimated_entry_cost_cents"], 88)
        self.assertLessEqual(result["estimated_entry_cost_cents"], 100)

    def test_returns_unavailable_when_no_contract_fits_budget(self):
        result = calculate_settlement_economics(80, 0.50, 2)
        self.assertFalse(result["available"])
        self.assertIn("does not cover one contract", result["reason"])

    def test_invalid_or_no_margin_inputs_fail_closed(self):
        self.assertFalse(calculate_settlement_economics(None, 1.00, 2)["available"])
        self.assertFalse(calculate_settlement_economics(98, 1.00, 2)["available"])
        self.assertFalse(calculate_settlement_economics(80, 1.00, -1)["available"])


if __name__ == "__main__":
    unittest.main()
