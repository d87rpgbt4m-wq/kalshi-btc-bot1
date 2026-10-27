import unittest

from btc_exit_policy import should_exit_on_trailing_retrace


class TakeProfitPatiencePolicyTests(unittest.TestCase):
    def test_enabled_trailing_exit_closes_on_retrace(self):
        self.assertTrue(should_exit_on_trailing_retrace(75.9, 76.0, enabled=True))

    def test_patient_mode_ignores_retrace_only(self):
        self.assertFalse(should_exit_on_trailing_retrace(75.9, 76.0, enabled=False))

    def test_bid_above_floor_does_not_exit(self):
        self.assertFalse(should_exit_on_trailing_retrace(76.1, 76.0, enabled=True))

    def test_invalid_quote_or_floor_fails_closed_without_exiting(self):
        self.assertFalse(should_exit_on_trailing_retrace(None, 76.0, enabled=True))
        self.assertFalse(should_exit_on_trailing_retrace(float('nan'), 76.0, enabled=True))


if __name__ == "__main__":
    unittest.main()
