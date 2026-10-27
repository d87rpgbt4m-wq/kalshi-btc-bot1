KALSHI BTC BOT — TRANSFER BUNDLE
================================

CONTENTS
--------
• 121-file full source snapshot saved on 2026-10-24.
• A separate RECOVERY_PATCH_2026-10-26 folder containing a small BTC strategy-gate patch saved on 2026-10-26.
• Transfer notes and validation material.

SOURCE-VERSION LIMITATION
-------------------------
This is NOT a byte-for-byte export of the latest Render deployment. During the export attempt on 2026-10-26, GitHub returned HTTP 403 because the owner account was suspended, and the latest source could not be fetched. The current Render services were verified to run newer October 26 source and the production database contains newer strategy-evolution state absent from this bundle.

Do not replace a running Render service with this October 24 snapshot. Recover the current source first, then apply the reviewable BTC patch. The recovery patch is not automatically wired into the baseline app.

SOURCE CONTROL AND RENDER
-------------------------
Use a private GitLab project as the GitHub replacement. Render supports GitLab. Before changing Render's source setting, confirm that the GitLab project exactly matches the deployed revision plus reviewed changes; changing the source triggers deployment. Preserve existing services, database, URLs, commands, and secrets. Keep all services paper-only with real orders disabled.

See GITLAB_RENDER_MIGRATION.md for the audited status, experiment findings, and careful migration sequence. The included .gitlab-ci.yml is a GitLab pipeline template; the existing .github folder is retained as historical snapshot content, not a requirement to use GitHub.

SECRETS
-------
Do not commit personal/vendor keys, .env files, private key files, or generated secret bundles. Set secrets in Render's environment settings only after restoring the correct source. Keep LIVE_TRADING_ENABLED=false and TRADING_MODE=paper.
