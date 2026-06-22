# Recovery Log

| Timestamp | Asset | Failure Mode | Action Taken | Rollback | Fallback | Validation | Residual Risk |
|---|---|---|---|---|---|---|---|
| 2026-06-21T11:45:00 | NPM Build | TypeScript strict mismatch | Replaced code directly | No | No | Build Passed | None |
| 2026-06-21T11:51:00 | Playwright MCP Install | `__dirlock` collision | Removed lockfile and retried install | No | No | Failed Again | High |
| 2026-06-21T11:59:00 | Playwright MCP Install | `__dirlock` persistent | OPEN CIRCUIT BREAKER. Installation suspended. | No | Yes | N/A | Low |
