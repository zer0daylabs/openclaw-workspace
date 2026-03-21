# CB Knowledge: Prisma ORM

Proficiency: **working** (updated 2026-03-21)

---

## What is Prisma?

Prisma ORM is a next-generation TypeScript/Node.js ORM that provides **type-safe database access**, **automated migrations**, and **Prisma Studio** (GUI). It's used in MusicGen and AudioStudio for database operations.

**Core Components:**
1. **Prisma Client** - Auto-generated, type-safe query interface
2. **Prisma Migrate** - Database migration system
3. **Prisma Studio** - Visual data editor

---

## Key Advantages

- ✅ **Type-safe queries** validated at compile time with full autocompletion
- ✅ **Plain JavaScript objects** returned (no complex model instances)
- ✅ **Single source of truth** - Prisma schema defines models
- ✅ **Prevents N+1 problems** through healthy constraints
- ✅ **Works with** Postgres, MySQL, SQLite, SQL Server, Oracle, MongoDB

---

## Core Workflow

### 1. Define Schema (`prisma/schema.prisma`)

```prisma
datasource db {
  provider = "postgresql"  // MusicGen/AudioStudio use Postgres
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id      Int    @id @default(autoincrement())
  email   String @unique
  name    String?
  posts   Post[]
  createdAt DateTime @default(now())
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User?    @relation(fields: [authorId], references: [id])
  authorId  Int?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

**Common Field Modifiers:**
- `@id` - Primary key
- `@default(value)` - Default value
- `@unique` - Unique constraint
- `@relation()` - Foreign key relationship
- `@map("column_name")` - Database column override
- `@updatedAt` - Auto-update timestamp

**Relation Types:**
- **One-to-one:** `User.profile Profile?`
- **One-to-many:** `User.posts Post[]`
- **Many-to-many:** `students Student[] @relation("Enrolled", references: [id])`

---

### 2. Generate Client

```bash
# Generate Prisma Client from schema
npx prisma generate
```

Generates `@prisma/client` package with full TypeScript types.

---

### 3. Run Migrations

```bash
# Create new migration from schema changes
npx prisma migrate dev --name describe_migration_name

# Apply migrations to database
npx prisma migrate deploy  # Production

# Reset database (development only)
npx prisma migrate reset
```

Migrations are stored in `prisma/migrations/` and version-controlled.

---

### 4. Query with Prisma Client

```typescript
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

// Find many users with posts
const users = await prisma.user.findMany({
  include: { posts: true }
})

// Find user by email
const user = await prisma.user.findUnique({
  where: { email: "alice@example.com" }
})

// Create user with nested post creation
const user = await prisma.user.create({
  data: {
    email: "alice@example.com",
    name: "Alice",
    posts: {
      create: { 
        title: "Hello World", 
        content: "First post" 
      }
    }
  },
  include: { posts: true }
})

// Update only specific fields
await prisma.user.update({
  where: { id: 1 },
  data: { name: "Alice Smith" }
})

// Delete user
await prisma.user.delete({
  where: { id: 1 }
})

// Raw query (when needed)
const result = await prisma.$queryRaw`
  SELECT * FROM users WHERE email = ${email}
`
```

**Query Filters:**
```typescript
// Where conditions
where: { 
  email: { contains: "test" }       // LIKE %test%
  id: { gt: 10 }                    // > 10
  OR: [{ status: "active" }, { status: "pending" }]  // OR
  AND: { published: true, authorId: 1 }               // AND
}

// Sorting
orderBy: { createdAt: "desc" }

// Pagination
take: 10    // LIMIT 10
skip: 20    // OFFSET 20

// Select specific fields
select: { id: true, email: true }  // only return these fields
```

---

## MusicGen/AudioStudio Context

Based on Vercel deployment findings (2026-03-08):
- Both apps use Railway-hosted Postgres databases
- DATABASE_URL env var NOT configured in Vercel (integration gap!)
- Database projects: `lucky-playfulness`, `truthful-warmth`, `appealing-laughter`

**Key Models Likely:**
- `User` - Platform users, subscriptions
- `Post` - Music tracks/audio content
- `Subscription` - Stripe billing data
- `Analytics` - Usage metrics

---

## Common Patterns & Best Practices

### 1. Connection Management
```typescript
// Singleton pattern (production-ready)
let cachedPrisma: PrismaClient

if (cachedPrisma) {
  return cachedPrisma
}

cachedPrisma = new PrismaClient({
  log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error']
})

export default cachedPrisma
```

### 2. Transaction Safety
```typescript
// Ensure atomicity for related operations
const result = await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data: { email: "test@test.com" } })
  const post = await tx.post.create({
    data: { title: "Test", authorId: user.id }
  })
  return { user, post }
})
```

### 3. Error Handling
```typescript
try {
  await prisma.user.create({ data: { email: "duplicate@test.com" } })
} catch (error) {
  if (error.code === "P2002") {
    console.log("Unique constraint violation")
  } else if (error.code === "P2025") {
    console.log("Record not found")
  }
}
```

**Common Error Codes:**
- `P2002` - Unique constraint violation
- `P2025` - Record not found
- `P2003` - Foreign constraint violation
- `P2015` - Relation query issue

---

## Common Pitfalls

1. **N+1 queries** - Use `include` or `distinct` to batch
2. **Over-fetching** - Use `select` to limit returned fields
3. **Missing indexes** - Add `@map("indexed")` for frequently queried fields
4. **Raw SQL injection** - Always use parameterized queries with `$queryRaw`
5. **Connection pool exhaustion** - Use singleton pattern, don't create new instance per request

---

## Tools & Utilities

### Prisma Studio
```bash
npx prisma studio
```
Opens localhost:5555 with visual database editor.

### Introspect Existing Database
```bash
npx prisma db pull  # Sync schema.prisma with existing DB
```

### Check SQL Generated
```bash
npx prisma format  # Format schema
npx prisma generate  # Regenerate client
```

### Performance Monitoring
```typescript
const prisma = new PrismaClient({
  log: [
    { level: 'query', emit: 'event' },
    { level: 'error', emit: 'stdout' },
    { level: 'warn', emit: 'stdout' }
  ]
})

prisma.$on('query', (e) => {
  console.log(`Query: ${e.query} | Params: ${e.params} | Duration: ${e.duration}ms`)
})
```

---

## Key Commands Cheat Sheet

```bash
# Development
npx prisma init                    # Initialize project
npx prisma generate                # Generate client
npx prisma migrate dev --name x    # Create & apply migration
npx prisma studio                  # GUI editor
npx prisma db pull                 # Introspect existing DB

# Production
npx prisma migrate deploy          # Apply migrations to prod
npx prisma generate                # Regenerate client for deploy

# Maintenance
npx prisma migrate reset           # Reset DB (dev only!)
npx prisma format                  # Format schema file
```

---

## Learning Resources

- [Prisma Documentation](https://www.prisma.io/docs)
- [Prisma Client API](https://www.prisma.io/docs/reference/api-reference/prisma-client-reference)
- [Prisma Schema Reference](https://www.prisma.io/docs/reference/api-reference/prisma-schema-reference)
- [Interactive Tutorial](https://www.prisma.io/docs/getting-started/quickstart)

---

## Status

- **Proficiency:** Basic → Working (after this research session)
- **Last Studied:** 2026-03-21
- **Practical Experience:** Know core workflow, schema design, query patterns, error handling, migrations
- **Ready For:** Database schema changes, migrations, debugging Prisma issues in MusicGen/AudioStudio
