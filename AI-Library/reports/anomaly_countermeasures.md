# Anomaly Countermeasures Register

This file acts as the permanent ledger for detected failure patterns and their permanent countermeasures as per the Phase 2 Operational Core directive.

## Log 001 - Telegram Webhook Conflict
- **Anomaly**: Telegram bot polling (`get_updates`) failed because a production Webhook was simultaneously active on the same token.
- **Impact**: Multi-agent Telegram bot became deaf and unresponsive to user commands.
- **Countermeasure**: Before initiating local Telegram bot polling, execute `deleteWebhook` API call. Ensure production deployments (e.g. Railway) use distinct tokens or handle local dev environments correctly.

## Log 002 - Next.js 16 ESM Conflict
- **Anomaly**: Turbopack compilation failed due to `package.json` defaulting to CommonJS while Next.js 16 enforces EcmaScript Modules internally.
- **Impact**: Total build failure during system update.
- **Countermeasure**: All new modular additions to `axyntrax-hud-nova` or `CRM_Gerencial` must explicitly enforce `"type": "module"` in their package configurations prior to compilation.
