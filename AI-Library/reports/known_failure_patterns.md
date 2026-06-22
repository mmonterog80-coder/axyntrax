# Known Failure Patterns

| ID | Category | Summary | Countermeasure | Owner |
|---|---|---|---|---|
| KFP-001 | REPEATED_FAILURE_PATTERN | Next.js 16 ESM conflict with package.json type | Always enforce `"type": "module"` when creating Next.js 16 packages | ANTIGRAVITY |
| KFP-002 | REPEATED_FAILURE_PATTERN | Webhook blocks Telegram Polling | Ensure `deleteWebhook` is called before starting local polling scripts | ANTIGRAVITY |
| KFP-003 | KNOWN_FRAGILITY | PowerShell String Escaping | Never use `Add-Content` with double quotes `"""` inside PowerShell strings. Always use `replace_file_content` tool. | ANTIGRAVITY |
