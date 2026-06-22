# Degraded Mode Status

**DEGRADED ASSETS:**
1. **Playwright MCP Server**: Global installation is repeatedly failing due to a persistent `__dirlock` collision in the npm cache. 
   - **Circuit State**: OPEN (Installation attempts suspended).
   - **Fallback Active**: Manual verification / Local browser fallback.

If an external API (such as Telegram Webhooks or GitHub Actions) fails, it will be listed here until the Circuit Breaker resets to CLOSED.
