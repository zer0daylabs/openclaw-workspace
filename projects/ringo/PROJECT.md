# Ringo - Task Management Platform

**Status:** In Development  
**Started:** 2026-03-06

## Overview

Ringo is a modern task management platform built for teams who need to get work done efficiently. Think of it as a streamlined alternative to Jira/Asana with a focus on speed and clarity.

## Tech Stack

- **Frontend:** Next.js 15 (App Router)
- **Database:** Supabase (PostgreSQL)
- **UI:** Tailwind CSS + shadcn/ui
- **Auth:** Supabase Auth (Email + Google OAuth)
- **Styling:** shadcn/ui components

## Core Features

### Priority 1 - Project Foundation
- [x] Project scaffolding
- [ ] Next.js 15 with App Router
- [ ] Supabase client setup
- [ ] Tailwind + shadcn/ui initialization
- [ ] Basic folder structure

### Priority 2 - Database Layer
- [ ] Projects table
- [ ] Tasks table
- [ ] Task Assignments table
- [ ] Users table (link to Supabase Auth)
- [ ] Row Level Security (RLS) policies
- [ ] Seed data

### Priority 3 - Authentication
- [ ] Email + password login
- [ ] Google OAuth integration
- [ ] Protected routes
- [ ] Session management

### Priority 4 - UI (Future)
- Dashboard view
- Project boards
- Task details
- Real-time updates

## Folder Structure (Planned)

```
projects/ringo/
├── app/
│   ├── (auth)/
│   │   └── login/
│   ├── (dashboard)/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── api/
│   └── layout.tsx
├── components/
│   ├── ui/ (shadcn)
│   └── shared/
├── lib/
│   ├── supabase/
│   └── utils.ts
├── supabase/
│   └── schema.sql
├── types/
│   └── index.ts
├── next.config.js
├── package.json
└── tsconfig.json
```

## Development Guidelines

1. **Type Safety:** Use TypeScript everywhere
2. **Database:** Write SQL first, then types
3. **Components:** Use shadcn/ui as base, customize minimally
4. **Auth:** Leverage Supabase Auth, no custom JWT handling
5. **RLS:** Secure by default, every table needs RLS policies

## Next Steps

1. Initialize project with Next.js 15 + Supabase
2. Define database schema with proper relationships
3. Implement auth flow
4. Build core UI components
5. Iterate based on feedback
