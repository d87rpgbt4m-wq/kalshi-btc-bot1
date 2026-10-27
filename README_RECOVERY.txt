KALSHI BTC BOT — UPDATED SOURCE BUNDLE

This archive contains the complete source tree from the user's supplied October 24, 2026 transfer bundle, with the BTC paper-trading and documentation changes prepared during this review.

It is the newest source copy available in this task, but it has NOT been deployed. The live Render services were last observed running newer October 26 code, and the production database contains newer strategy-evolution state not represented in this source tree. Treat this as the user's updated working baseline, not as a direct replacement for the live Render deployment.

BTC changes in this copy:
- Fixed paper stops default on at 35%; missing stop levels are initialized for open positions only.
- Trend-stop exits remain disabled; shadow mode defaults on.
- Routine take-profit trailing-retrace exits can be disabled for a paper patience experiment while other exit safeguards remain separate.
- The dashboard reports deterministic settlement payout, net profit, max loss, and break-even math.
- Added deterministic helper tests and GitLab CI/migration guidance.

Verification: 8 new helper tests and 19 focused existing checks passed; compile, inline dashboard JavaScript syntax, and patch applicability checks passed. The full paper-worker test module could not import because the available Python runtime lacks requests.

For the current test phase, no paid database upgrade is needed. Keep the existing test database if you want its paper history; decide about export or durable storage before live trading if you want to retain that history. Recover/reconcile the running source, run CI in a private GitLab project, and keep real-money trading disabled. Changing a Render source repository can automatically start a deployment.
