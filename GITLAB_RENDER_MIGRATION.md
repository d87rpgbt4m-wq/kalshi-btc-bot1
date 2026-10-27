# BTC Bot: GitLab and Render recovery plan

## Current source status

The supplied bundle contains a 121-file source snapshot from October 24, 2026. The latest Render deployment inspected on October 26 runs commit `a893c74f3d7d34a43cdc0a49ba1ba40c9e4a2b02` from October 26, 2026 at 07:54 UTC. The current production database also contains strategy-evolution tables and candidate state absent from this bundle.

**Do not connect this October 24 snapshot as a full replacement for the running services.** It could roll production back and remove newer strategy-learning, dashboard, or schema work. First recover a faithful export of the deployed/current source, then apply the source changes in this patch kit. GitHub could not provide the current source because the account was suspended.

## Latest live BTC paper state

- Latest database check after settlement: 175 settled trades, 100 positive, 74 negative, 1 breakeven; net realized P&L -95.6 cents after fees. The screenshot shared earlier showed 174 trades and -$1.03.
- Recent worker logs showed fixed stops disabled, trend-stop execution disabled, and trend-stop shadow mode disabled. 136 of 175 settled rows had no stored fixed-stop level.
- Adaptive entry preference is still 80 cents, with zero automatic tightenings. Its most recent review covered 120 evaluations, sample 20, and -41.8 cents net, then awaited 10 additional newer settled hybrid trades.
- A separate strategy-evolution system has 15 candidates; none is promoted. Its latest prospective review had 25 opportunities toward the 30-opportunity initial validation threshold.
- The shared PostgreSQL database is on a free plan scheduled to expire November 21, 2026 at 23:47 UTC. The user confirmed this test bot does not need a paid database now. This is not a blocker; revisit database retention before any move to live trading.
- Current paper safeguards show maximum cost per trade $1, daily loss limit $10, preferred entry 80 cents, and hard cap 92 cents. There were no open positions at the last database check.

Win rate alone is not the target. The bot had 100 wins in 175 settlements while net P&L was negative. Compare fee-adjusted P&L, average win and loss, drawdown, and positive-net rate on the same prospective signals.

## Strategy comparisons from the latest review

The live evolution engine compared the same 25 recent opportunities:

| Candidate | Trades | W/L | Net | Per opportunity | Paired 95% lower bound |
|---|---:|---:|---:|---:|---:|
| Baseline | 25 | 17/8 | -84.8¢ | -3.39¢ | — |
| Aligned trend + confirmed volume | 5 | 4/1 | +102¢ | +4.08¢ | -6.68¢ |
| Aligned trend | 7 | 5/2 | +81¢ | +3.24¢ | -7.10¢ |
| Confirmed volume | 15 | 11/4 | +75¢ | +3.00¢ | -3.47¢ |

Aligned trend plus confirmed volume led this small sample, but every candidate's lower bound still allows negative results. Keep all candidates in paper comparison; do not automatically promote one from this data.

A separate exploratory filter on the same recent opportunities showed entries at or below 64 cents: 7 trades, 5W/2L, +158 cents, with approximate paired lower bound -5.25 cents per opportunity. Entries at or below 75 cents lost 49 cents over 14 trades. This retrospectively selected, small cohort is not a production rule.

Across 175 actual settlements by entry ask: under 50 cents lost 87.4 cents across 19; 50–64 cents gained 177.2 cents across 53; 65–79 cents lost 150.4 cents across 71; 80–92 cents lost 35 cents across 32. These descriptive buckets do not establish causal thresholds.

## Exit and position-size experiments

The exit audit matched actual trades to a reconstructed one-contract hold-to-settlement result, scaled by actual contract count. It assumes settlement at the recorded outcome and is not a guaranteed executable fill:

| Actual exit | Paired | Actual net | Hold-to-settlement | Relative result |
|---|---:|---:|---:|---|
| Take profit | 18 | +130.6¢ | +414.0¢ | Hold model +283.4¢; hold higher on 14/18 |
| Trend stop | 60 | -1,156.7¢ | -1,609.0¢ | Actual exits +452.3¢; exit higher on 32/60 |
| Fixed stop | 20 | -774.4¢ | -753.0¢ | Hold model +21.4¢ total; actual exit higher on 15/20 |

This supports a **paper-only patient take-profit comparison**: do not exit solely because the bid retraced below a routine trailing take-profit floor. Keep fixed stops, strong reversal/profit-protection exits, and settlement. Keep chart-trend stop shadow-only while collecting prospective matched evidence; its retrospective counterfactual was mixed but better in aggregate than holding. Never assume a stop trigger guarantees the modeled fill price.

A historical sizing replay compared the current $1 maximum-cost rule with one contract per trade. One contract reduced maximum drawdown from 687.8 to 612.4 cents and the worst realized loss from 94 to 84 cents, but net P&L was 33.9 cents worse. Do not scale up; compare drawdown and net returns prospectively.

## Stop behavior prepared in the snapshot patch

The patch makes fixed paper stops default on at 35% below entry and initializes a missing stop for an already-open position. It does not rewrite settled history. Chart-trend stop execution remains off and shadow mode defaults on. Routine trailing take-profit retraces can be ignored for a patient-hold paper candidate; fixed stop, reversal/profit-protection, trend-stop, and settlement logic remain separate.

TradingView stays the external direction and alert source. The bot should compare each eligible signal using the existing freshness, market-window, quote, spread, fee, exposure and risk checks, plus trend/momentum alignment, confirmed volume, market regime, distance to strike, time remaining, entry ask, and alert age. Record both accepted and rejected signal reasons. The internal heuristic score is not a calibrated win probability.

## Settlement payout math and the $1.33 question

The uploaded dashboard code did not include a displayed $1.33 estimate, so its source cannot be identified from the supplied snapshot. The new paper dashboard card reports deterministic settlement mechanics and explicitly does not forecast win probability.

For one standard binary contract bought at 80 cents with a configured 2-cent entry fee: total cost is 82 cents; a correct settlement pays $1 gross, or +18 cents net; an incorrect settlement pays $0, or -82 cents; break-even probability is 82%. A 58% score is not a calibrated 58% chance. If it were a true probability, this price/fee combination has expected net value of -24 cents per contract. The dashboard must keep payout, profit, loss, and probability clearly separate.

Sources: [Kalshi payout and positions](https://help.kalshi.com/en/articles/13823844-portfolio-balances-and-positions), [Kalshi fee schedule](https://kalshi.com/fee-schedule).

## Moving Render source from GitHub to GitLab

Render supports GitLab as a Git provider and changing a service's source repository in its Dashboard automatically starts a deploy. Prepare and verify the exact current source in GitLab first.

1. Create a private GitLab project under an account you control. Import the complete current source only after confirming it matches the running revision and includes strategy-evolution code and schema changes. Never upload keys, `.env` files, or generated secret bundles.
2. Add the included `.gitlab-ci.yml` and confirm its pipeline passes on the exact commit intended for production. Render's GitLab integration needs Maintainer or Owner access.
3. Connect the authorized GitLab account in Render under Account Settings / Git Providers.
4. For each existing Render service — dashboard, BTC worker, and market-analysis provider — use Settings → Build → Source → Edit and select the same private project and branch. The source change triggers a deploy. Preserve service type, commands, URLs, disks, and environment.
5. For the current test phase, keep using the existing PostgreSQL database and its `DATABASE_URL` on web and worker if continuing the current paper history. No paid upgrade is needed now. Do not create a replacement database or change schema before recovering and reviewing the current source. Revisit durable storage before live trading if the history should be retained.
6. Set worker variables to `PAPER_STOP_LOSS_ENABLED=true`, `PAPER_STOP_LOSS_PERCENT=35`, `PAPER_TREND_STOP_LOSS_ENABLED=false`, and `PAPER_TREND_STOP_SHADOW_MODE=true`. Keep `TRADING_MODE=paper`, `LIVE_TRADING_ENABLED=false`, and live approval flags false.
7. Verify startup logs report the fixed-stop configuration, newly opened paper trades store a stop, and shadow triggers do not settle positions. Investigate missing stop values before treating the fix as complete.
8. Enable Render auto-deploy only after CI passes for the selected source. Keep real-order routes disabled.

The Render environment update attempted during this audit was rejected because Render could not access the GitHub repository. No environment changes or deployment were applied.

The free database is scheduled to expire November 21, 2026 at 23:47 UTC. The user has said this is acceptable during the test phase and does not want to pay for an upgrade now. Free database data can become inaccessible at expiration and is eventually deleted after Render's grace period. Revisit backup or a paid plan before live trading if preserving the paper history matters.

References: [Render Git providers](https://render.com/docs/git-provider), [Render deploys and CI checks](https://render.com/docs/deploys), [changing a service's backing repository](https://render.com/changelog/change-your-services-backing-repo-or-image-in-the-render-dashboard).

