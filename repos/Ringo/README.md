# Ringo MVP

A lightweight MVP for the Ringo lead management platform. The application is a Next.js 14 full‑stack project with:

- **Prisma** as the database ORM (PostgreSQL).
- **Redis** for caching route decisions and rate‑limits.
- **Stripe** for billing and payouts.
- **OpenAI LLM** integration for AI screening.
- A small buyer portal built with React‑Server Components and TS.
- Basic authentication using JWT.

## Getting Started

```bash
# Clone and navigate
cd /home/lauro/.openclaw/workspace/repos/Ringo

# Install dependencies
npm install

# Set up the database (you'll need PostgreSQL running)
cp .env.example .env
# edit .env to set your DATABASE_URL, JWT_SECRET, etc.

# Generate Prisma client
npm run prisma:generate

# Run migrations
npm run prisma:migrate

# Start development server
npm run dev
```

## API Endpoints

- `POST /api/auth/register` – Register a new buyer.
- `POST /api/auth/login` – Login and receive JWT.
- `POST /api/calls/route` – Public endpoint to route a call.
- `POST /api/calls/screen` – Public endpoint for AI screening.
- `POST /api/calls/complete` – Callback when a call ends.
- Buyer‑only routes under `/api/buyers/*`.

## Testing

Run Jest tests:

```bash
npm test
```

## License

MIT.
