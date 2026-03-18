# Sentry — CB Knowledge Summary

Last updated: 2026-03-18
Proficiency: basic
Source: Sentry Documentation, integration guides

## What It Is
Sentry is **developer-first error tracking and performance monitoring**. It automatically reports errors, uncaught exceptions, and unhandled rejections. Core feature is Issues (always enabled). Additional features: Tracing, Session Replay, Logs, User Feedback.

## Architecture
- **Core purpose:** Automatic error capture and performance tracing
- **Integration:** Browser tracing, server-side instrumentation
- **Distributed tracing:** Follow requests from frontend to backend and back
- **Features:**
  - **Issues:** Core error monitoring (always enabled)
  - **Tracing:** Track performance, distributed tracing
  - **Session Replay:** Video-like reproduction of user's browser before error
  - **Logs:** Log aggregation
  - **User Feedback:** Collect user reports

## Our Use Case
**Zer0Day Labs products (MusicGen, AudioStudio)** need Sentry for:
1. **Error tracking** in production - automatically capture exceptions, unhandled rejections
2. **Performance monitoring** - identify slow endpoints, bottlenecks
3. **Alert configuration** - get notified of critical errors immediately
4. **Source maps** - link minified errors back to original source code
5. **CI/CD automation** - upload source maps during deployment

## Key Commands / API
- **Install:** `npm install @sentry/react --save`
- **Initialize:**
```javascript
Sentry.init({
  dsn: 'https://<key>@sentry.io/<project>',
  // Enable automatic instrumentation (highly recommended)
  integrations: [Sentry.browserTracingIntegration()],
  tracesSampleRate: 1.0,
  tracePropagationTargets: ['localhost', /^https://yourserver.io/api/],
});
```
- **Next.js:** Use dedicated SDK instead of React SDK
- **Manual instrumentation:** Remove BrowserTracing integration + call Sentry.addTracingExtensions()

## Configuration
- **Best practices:**
  - Source map uploads during CI/CD
  - Adjust tracesSampleRate for performance (1.0 = 100% sampling)
  - Configure tracePropagationTargets for distributed tracing
  - Use error boundaries for automatic error capture
  - Integrate with React Router and Redux for deep insights
- **Alert configuration:**
  - Configure alerts for every new error event
  - Customize alert frequency per team needs
  - Create default alert rules for all new issues
  - Issue Alert Configuration via Sentry UI

## Integration Points
- **Next.js:** Dedicated SDK for server-side rendering
- **React:** @sentry/react for client-side SPA
- **CI/CD:** Upload source maps during deployment
- **Vercel:** Auto-detects Sentry, easy integration
- **React Router:** Deep integration for routing insights
- **Redux:** State change tracking

## Gotchas
- **React Server Components/SSR:** Use Next.js/Remix/Gatsby dedicated SDK instead of React SDK
- **Performance impact:** Adjust tracesSampleRate in production (1.0 may be too high)
- **Source maps:** Must upload during CI/CD for readable error stacks
- **Alert rules:** Default alerts exist, but should be customized for team needs
- **Alert frequency:** Can configure to prevent alert fatigue
- **BrowserTracing:** Optional - remove for purely manual instrumentation

## Resources
- **Sentry Docs:** https://docs.sentry.io/
- **React Integration:** https://docs.sentry.io/platforms/javascript/guides/react/
- **Next.js Integration:** https://docs.sentry.io/platforms/javascript/guides/nextjs/
- **Alert Configuration:** https://docs.sentry.io/product/alerts/create-alerts/issue-alert-config/
- **Alerts Overview:** https://docs.sentry.io/product/alerts/

## Current Proficiency Assessment
- **Status:** Research complete (2026-03-18)
- **Gap identified:** Need deeper understanding of alert configuration patterns
- **Action:** Create alert rules for Zer0Day Labs products
- **Next steps:** Configure alerts for critical errors, set up notification channels, establish baseline metrics

## Manual Action Required
**Setup Sentry monitoring alerts (35-45 min):**
1. Create Sentry account/project for Zer0Day Labs
2. Install @sentry/react in MusicGen and AudioStudio
3. Configure DSN, tracesSampleRate, integrations
4. Set up source map upload in CI/CD
5. Configure issue alerts for critical errors
6. Set up notification channels (Slack, email)
7. Establish baseline metrics and thresholds