# Preventive Alerts Register

## EARLY ALERT
- **Issue**: No automated UI tests detected in Next.js builds.
- **Evidence**: `npm run build` runs successfully, but there are no Playwright test scripts configured in `package.json` for either `CRM_Gerencial` or `axyntrax-hud-nova`.
- **Impact**: UI regressions could be deployed to Vercel/production without prior detection.
- **Urgency**: Moderate
- **Safe Next Action**: Configure a basic Playwright test suite for both frontend applications and add to the `build` script.
- **Stored in Memory**: Yes (Pending execution)
