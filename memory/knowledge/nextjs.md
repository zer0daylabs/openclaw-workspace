# Next.js — CB Knowledge Summary

Last updated: 2026-03-15
Proficiency: working
Source: MusicGen, AudioStudio, Ringo codebases

## What It Is
React-based full-stack web framework by Vercel. Supports SSR, SSG, API routes, middleware, and edge functions.

## Architecture
- File-based routing (app/ directory in Next.js 13+)
- Server components by default, client components with "use client"
- API routes in app/api/ directory
- Middleware in middleware.ts at root
- Built-in image optimization, font optimization
- Prisma typically used as ORM layer

## Our Use Case
- **MusicGen** (edmmusic.studio) — Music generation SaaS
- **AudioStudio** (audiostudio.ai) — Audio processing SaaS
- **Ringo** — TBD project
- All deployed on Vercel (team: zer0day)
- All use TypeScript, Tailwind CSS, Prisma

## Key Commands
```bash
# Development
npm run dev          # Start dev server (port 3000)
npm run build        # Production build (catches type errors)
npm run start        # Start production server
npx tsc --noEmit     # Type check without building

# Prisma
npx prisma generate  # Regenerate client after schema change
npx prisma db push   # Push schema to database
npx prisma studio    # Visual database browser
```

## Configuration
- `next.config.js` — Framework config
- `tsconfig.json` — TypeScript config
- `tailwind.config.ts` — Tailwind theme
- `.env.local` — Environment variables (gitignored)
- `prisma/schema.prisma` — Database schema

## Integration Points
- Vercel: auto-deploys from GitHub on push
- Railway: PostgreSQL databases (need DATABASE_URL in Vercel env vars)
- Stripe: payment processing via webhooks
- Sentry: error tracking (setup pending)
- PostHog: analytics (setup pending)

## Gotchas
- Server vs client component boundary — "use client" needed for hooks/interactivity
- Environment variables: NEXT_PUBLIC_ prefix required for client-side access
- API routes run serverless — cold starts, no persistent connections
- Prisma in serverless: need connection pooling (PgBouncer or Prisma Accelerate)
- `npm run build` is the real type check — dev mode is lenient
- Vercel has function size limits (50MB default)

## Resources
- Docs: https://nextjs.org/docs
- App Router: https://nextjs.org/docs/app
- API Routes: https://nextjs.org/docs/app/building-your-application/routing/route-handlers
