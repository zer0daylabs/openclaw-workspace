# Ringo – Complete Backend Technical Specification
**Version:** 2026-03-05 (Final AI-Enhanced)  
**Author:** CB (Zer0Day Labs)  
**Scope:** AI-enhanced pay-per-call marketplace with dynamic lead-category routing

---

## 1. Executive Summary

Ringo is a real-time bidding marketplace where:

- **Buyers** purchase leads by **lead category** (e.g., personal auto insurance, commercial health plans)
- **AI pre-screening** intercepts every inbound call, transcribes in real-time, classifies lead intent, and captures structured data
- The system routes the call to the **highest bidder for the classified lead category**
- Even if the call drops, the AI enriches and stores a complete lead package that can be sold later
- **Dynamic bidding** with per-category premiums and volume quotas

**Key Differentiators:**
- Sub-50ms routing latency through Redis caching
- AI-powered lead classification and enrichment
- Per-category bidding with quotas
- Same-day payouts via Stripe
- Lead data retention (sell dropped call leads)

---

## 2. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    Ringo Frontend (Next.js)                      │
│                  Buyer Dashboard & Seller Portal                 │
└──────────────────────────────────────────────────────────────────┘
                                      │
                                      │ REST/GraphQL APIs
                                      ▼
┌──────────────────────────────────────────────────────────────────┐
│                        API Gateway                               │
│           (Auth, Rate-Limit, Logging, Webhook Handling)          │
└──────────────────────────────────────────────────────────────────┘
         │                    │                    │
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Buyer API  │    │   Seller API    │    │  Routing API    │
└─────────────┘    └─────────────────┘    └─────────────────┘
         │                    │                    │
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Redis     │    │   PostgreSQL    │    │   Redis Cache   │
│ (Sessions)  │    │   (Prisma ORM)  │    │ (Routing Lookup)│
└─────────────┘    └─────────────────┘    └─────────────────┘
         │                    │                    │
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Stripe SDK │    │  AI Service     │    │  Webhooks       │
│(Payments)   │    │ (LLM + STT)     │    │ (Events)        │
└─────────────┘    └─────────────────┘    └─────────────────┘
         │                    │                    │
         │                    │                    │
         └────────────────────┴────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────┐
│              Telephony Engine (Own 1M+ Numbers)                  │
│           Inbound → AI Screening → Category → Route              │
└──────────────────────────────────────────────────────────────────┘
```

**Technology Stack:**
- **Frontend:** Next.js (shared with MusicGen/AudioStudio)
- **Backend:** Node.js API services (Next.js API routes)
- **Database:** PostgreSQL (Railway) + Prisma ORM
- **Cache:** Redis (fast routing lookups, AI result caching)
- **Payments:** Stripe SDK (payments, instant payouts)
- **AI:** Whisper AI (STT) + LLM (intent classification, data extraction)
- **Telephony:** Internal VoIP infrastructure (own 1M+ numbers)

---

## 3. Database Schema (Prisma)

```prisma
// ==================== PRISMA SCHEMA ====================

generator client {
  provider = "prisma-client-js"
  previewFeatures = ["postgresqlExtensions"]
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
  extensions = [ "btree_gin", "uuid-ossp" ]
}

// ============================================
// USER & AUTHENTICATION
// ============================================

model User {
  id                String       @id @default(uuid())
  email             String       @unique
  passwordHash      String
  createdAt         DateTime     @default(now())
  lastLoginAt       DateTime?
  type              UserType     @default(BUYER)
  phoneNumbers      PhoneNumber[] @relation("PhoneNumberOwner")
  campaigns         Campaign[]
  billingProfile    BillingProfile?
  creditBalanceCents BigInt       @default(0)
  isActive          Boolean      @default(true)
  createdBy          String?      @db.VarChar(255)
  
  // Relations
  bids              Bid[]
  callLogsAsBuyer   CallLog[]     @relation("BuyerRelationship")
  enrichmentData    LeadEnrichment[]
}

enum UserType { BUYER SELLER ADMIN }

model BillingProfile {
  id           String       @id @default(uuid())
  userId       String       @unique
  stripeCustId String       @unique
  stripeAccId  String?
  user         User         @relation(fields: [userId], references: [id])
  createdAt    DateTime     @default(now())
}

// ============================================
// PHONE NUMBERS & OWNERSHIP
// ============================================

model PhoneNumber {
  id          String       @id @default(uuid())
  number      String       @unique
  ownerId     String?
  owner       User?        @relation(fields: [ownerId], references: [id])
  status      NumberStatus @default(AVAILABLE)
  assignedTo  Seller?      @relation(fields: [ownerId], references: [id])
  metadata    Json?
  createdAt   DateTime     @default(now())
  updatedAt   DateTime     @updatedAt
  
  // Relations
  callLogs    CallLog[]
}

enum NumberStatus { AVAILABLE IN_USE INACTIVE }

// ============================================
// CATEGORIES & CHANNELS (Hierarchical)
// ============================================

model Category {
  id          String       @id @default(uuid())
  name        String       @unique
  parentId    String?      @db.VarChar(36)  // null for top-level categories
  parent      Category?    @relation("CategoryHierarchy", fields: [parentId], references: [id])
  children    Category[]   @relation("CategoryHierarchy")
  description String?
  premium     Int          @default(0)      // base premium per minute for this category
  createdAt   DateTime     @default(now())
  
  // Relations
  campaigns   Campaign[]
  bids        Bid[]
  leadCategories LeadCategory[]
}

model Channel {
  id          String       @id @default(uuid())
  name        String       @unique
  description String?
  createdAt   DateTime     @default(now())
}

// ============================================
// CAMPAIGNS & ROUTING RULES
// ============================================

model Campaign {
  id           String       @id @default(uuid())
  name         String
  ownerId      String
  owner        User         @relation(fields: [ownerId], references: [id])
  channel      Channel
  channelId    String
  category     Category
  categoryId   String
  bidAmountCents Int          // default per-call bid
  volumeQuota   Int          // max calls per period
  isActive      Boolean      @default(true)
  createdAt     DateTime     @default(now())
  updatedAt     DateTime     @updatedAt
  
  // Relations
  routingRules  RoutingRule[]
  bids          Bid[]
  enrichmentData LeadEnrichment[]
}

model RoutingRule {
  id          String       @id @default(uuid())
  campaignId  String
  campaign    Campaign     @relation(fields: [campaignId], references: [id], onDelete: Cascade)
  condition   Json         // e.g., { "geo": ["US", "CA"], "time": "09:00-17:00" }
  priority    Int          @default(1)
  active      Boolean      @default(true)
  createdAt   DateTime     @default(now())
}

// ============================================
// BIDDING SYSTEM (Per-Category)
// ============================================

model Bid {
  id           String       @id @default(uuid())
  campaignId   String
  campaign     Campaign     @relation(fields: [campaignId], references: [id])
  userId       String
  user         User         @relation(fields: [userId], references: [id])
  amountCents  Int          // bid per call or per minute
  categoryId   String
  category     Category     @relation(fields: [categoryId], references: [id])
  quota        Int          @default(0)  // max calls/month for this category
  usedQuota    Int          @default(0)
  status       BidStatus    @default(PENDING)
  createdAt    DateTime     @default(now())
  updatedAt    DateTime     @updatedAt
  
  // Relations
  callLogsAsBuyer CallLog[] @relation("BuyerRelationship")
}

enum BidStatus { PENDING ACCEPTED DECLINED EXPIRED }

// ============================================
// LEAD CATEGORIES (AI Classification)
// ============================================

model LeadCategory {
  id          String       @id @default(uuid())
  name        String       @unique
  description String?
  premiumRate Int          @default(0)      // premium rate for this lead type
  createdAt   DateTime     @default(now())
  
  // Relations
  callLogs    CallLog[]
  enrichments LeadEnrichment[]
}

// ============================================
// CALL LOGS & LEAD ENRICHMENT
// ============================================

model CallLog {
  id                String       @id @default(uuid())
  inboundNumberId   String
  inboundNumber     PhoneNumber  @relation(fields: [inboundNumberId], references: [id])
  buyerId           String?
  buyer             User?        @relation("BuyerRelationship", fields: [buyerId], references: [id])
  timestamp         DateTime     @default(now())
  durationSeconds   Int          @default(0)
  status            CallStatus   @default(QUALIFIED)
  costCents         Int          @default(0)
  revenueCents      Int          @default(0)
  aiScore           Float?
  leadCategoryId    String?
  leadCategory      LeadCategory? @relation(fields: [leadCategoryId], references: [id])
  enrichedData      Json?        // structured lead package
  metadata          Json?
  createdAt         DateTime     @default(now())
  updatedAt         DateTime     @updatedAt
  
  // Relations
  leadEnrichment    LeadEnrichment?
  callsAsSeller     PhoneNumber[] @relation("SellerCalls")
}

enum CallStatus { CONNECTED DROPPED NO_ANSWER QUALIFIED FAILED }

// ============================================
// AI-ENRICHED LEAD DATA
// ============================================

model LeadEnrichment {
  id             String       @id @default(uuid())
  callLogId      String       @unique
  callLog        CallLog      @relation(fields: [callLogId], references: [id])
  leadCategory   LeadCategory
  leadCategoryId String
  intent         String
  sentiment      Float        // -1.0 to 1.0
  qualified      Boolean
  score          Float        // 0.0 to 1.0
  structuredData Json         // name, phone, needs, budget, timeframe, etc.
  transcript     String?      @db.Text
  keywords       [String]
  createdAt      DateTime     @default(now())
}

// ============================================
// PAYMENT SYSTEM (Stripe)
// ============================================

model StripeCharge {
  id             String       @id @default(uuid())
  userId         String
  user           User         @relation(fields: [userId], references: [id])
  amountCents    Int
  stripeChargeId String       @unique
  createdAt      DateTime     @default(now())
  status         ChargeStatus @default(PENDING)
}

enum ChargeStatus { PENDING SUCCEEDED FAILED }

model StripePayout {
  id             String       @id @default(uuid())
  userId         String
  user           User         @relation(fields: [userId], references: [id])
  amountCents    Int
  stripePayoutId String       @unique
  createdAt      DateTime     @default(now())
  status         PayoutStatus @default(PENDING)
}

enum PayoutStatus { PENDING SUCCEEDED FAILED }

// ============================================
// INDEXES (Performance Optimization)
// ============================================

// Fast routing lookup by inbound number
@@index([number])
@@index([status])

// Fast call log queries for analytics
@@index([timestamp])
@@index([leadCategoryId])
@@index([buyerId])

// Fast bid lookup by category
@@index([categoryId])
@@index([status])

// Fast category queries
@@index([parentId])
@@index([name])
```

---

## 4. API Endpoints

### 4.1 Buyer Portal (JWT Required)

| Method | Path | Description | Request Body | Response |
|--------|------|-------------|--------------|----------|
| **FUNDING** |
| POST | `/api/buyers/fund` | Add credit via Stripe Checkout | `{ "amountCents": 10000, "currency": "usd" }` | `{ "sessionId": "cs_..." }` |
| **BIDDING** |
| POST | `/api/buyers/bids` | Create/update bid for specific lead category | `{ "campaignId": "uuid", "amountCents": 500, "categoryId": "uuid", "quota": 1000 }` | `{ "id": "uuid", "status": "PENDING" }` |
| GET | `/api/buyers/bids` | List buyer's bids with category details | Query: `{ page, limit, status }` | Paginated bid list |
| PUT | `/api/buyers/bids/:id` | Update existing bid | `{ "amountCents": 600, "quota": 1200 }` | Updated bid |
| DELETE | `/api/buyers/bids/:id` | Cancel bid | None | `{ "success": true }` |
| **ANALYTICS** |
| GET | `/api/buyers/analytics` | Performance by lead category | Query: `{ period: "7d|30d|90d", category?: "uuid" }` | Analytics object |
| GET | `/api/buyers/leads` | Retrieve enriched leads (including dropped calls) | Query: `{ page, limit, qualified: true|false, category?: "uuid" }` | Lead list with structured data |
| GET | `/api/buyers/leads/:leadId` | Get specific lead details | None | Lead object |
| GET | `/api/buyers/calls` | Call logs with lead details | Query: `{ page, limit, status, startDate, endDate }` | Call log list |
| **PAYOUTS** |
| POST | `/api/buyers/payouts` | Manual instant payout | `{ "amountCents": 5000 }` | `{ "payoutId": "po_..." }` |
| GET | `/api/buyers/payouts` | List payout history | Query: `{ page, limit, status }` | Payout list |

### 4.2 Seller Portal (JWT Required)

| Method | Path | Description | Request Body | Response |
|--------|------|-------------|--------------|----------|
| **PHONE NUMBERS** |
| POST | `/api/sellers/numbers` | Add owned number (admin only) | `{ "number": "+15551234567", "status": "IN_USE" }` | `{ "id": "uuid" }` |
| GET | `/api/sellers/numbers` | List owned numbers | Query: `{ page, limit, status }` | Number list |
| PATCH | `/api/sellers/numbers/:id` | Update number status | `{ "status": "INACTIVE" }` | Updated number |
| **CAMPAIGNS** |
| POST | `/api/sellers/campaigns` | Create campaign | `{ "name": "Auto Insurance", "channelId": "uuid", "categoryId": "uuid", "bidAmountCents": 500, "volumeQuota": 1000 }` | `{ "id": "uuid" }` |
| GET | `/api/sellers/campaigns/:id` | Campaign details | None | Campaign object |
| PUT | `/api/sellers/campaigns/:id` | Update campaign | Update fields | Updated campaign |
| DELETE | `/api/sellers/campaigns/:id` | Delete campaign | None | `{ "success": true }` |
| GET | `/api/sellers/campaigns` | List campaigns | Query: `{ page, limit }` | Campaign list |
| **ANALYTICS** |
| GET | `/api/sellers/analytics` | Sales & volume metrics | Query: `{ period: "7d|30d", category?: "uuid" }` | Analytics object |

### 4.3 Real-Time Routing API (Public - No JWT)

| Method | Path | Description | Request Body | Response |
|--------|------|-------------|--------------|----------|
| **ROUTE** |
| POST | `/api/calls/route` | AI screening trigger → returns route decision | `{ "inboundNumber": "+15551234567", "callerId": "+15559876543", "timestamp": "2026-03-05T13:00:00Z", "metadata?: { geo?: "US", timezone?: "America/Phoenix" }` | See AI Screening Response (below) |
| **SCREEN** |
| POST | `/api/calls/screen` | AI pre-screening endpoint (transcribes, classifies, extracts) | `{ "callId": "uuid", "audioStream": "base64", "metadata?: { callerId, geo, timezone }` | AI Screening Response (below) |
| **COMPLETE** |
| POST | `/api/calls/complete` | Call completion callback with AI results | `{ "callId": "uuid", "durationSeconds": 120, "status": "CONNECTED", "aiScore": 0.85, "structuredData?: {...}` | `{ "success": true }` |
| **LEAD RETRIEVAL** |
| GET | `/api/calls/leads/:leadId` | Retrieve lead enrichment data | None | `{ "id": "uuid", "callId": "uuid", "leadCategory": "Personal Auto", "structuredData": {...}, "score": 0.85, "transcript": "...", "keywords": [...] }` |

### 4.4 AI Screening Response Schema

```json
{
  "callId": "call-uuid-12345",
  "timestamp": "2026-03-05T13:00:00Z",
  "aiResults": {
    "leadCategory": "Personal Auto",
    "leadCategoryId": "cat-uuid-123",
    "intent": "personal auto insurance",
    "qualified": true,
    "score": 0.85,
    "sentiment": 0.72,
    "structuredData": {
      "name": "John Doe",
      "phone": "+15551234567",
      "needs": "need new auto insurance, current policy expiring",
      "budget": 1500,
      "timeframe": "within 2 weeks"
    },
    "transcript": "Caller expressed interest in personal auto insurance...",
    "keywords": ["auto", "insurance", "expiring", "budget"],
    "confidence": 0.92
  },
  "routing": {
    "winningBuyerId": "buyer-uuid",
    "winningBuyerName": "ABC Insurance",
    "destination": "sip:buyer@example.com",
    "effectiveBid": 500,
    "remainingQuota": 150,
    "fallbackDestination": "+15559998888"
  },
  "metadata": {
    "inboundNumber": "+15551234567",
    "callerId": "+15559876543",
    "geo": "US",
    "timezone": "America/Phoenix"
  }
}
```

### 4.5 Admin Endpoints (JWT Required - Admin Only)

| Method | Path | Description |
|--------|------|-------------|
| `GET /api/admin/users` | List all users |
| `PATCH /api/admin/users/:id` | Update user status |
| `GET /api/admin/phone-numbers/unused` | List unassigned numbers |
| `POST /api/admin/phone-numbers/bulk-assign` | Bulk assign numbers |
| `GET /api/admin/financials` | Revenue & payouts summary |
| `GET /api/admin/categories` | List all lead categories |
| `POST /api/admin/categories` | Create new category |
| `POST /api/admin/stripe/webhook` | Handle Stripe events |
| `GET /api/admin/audit-logs` | System audit logs |

---

## 5. Business Logic

### 5.1 AI Pre-Screening Flow

**Step 1: Real-Time STT**
- Stream audio from caller to STT service (Whisper AI)
- Transcribe in real-time, partial results returned continuously

**Step 2: Intent Classification**
- LLM analyzes transcript and caller intent
- Returns lead category: `"personal auto insurance"`, `"commercial health"`, `"financial planning"`, etc.

**Step 3: Structured Data Extraction**
- Extract specific fields:
  - Name (if mentioned)
  - Phone number (if different from caller ID)
  - Specific needs
  - Budget range
  - Timeframe (immediate, weeks, months)

**Step 4: Lead Scoring**
- AI score: 0.0 - 1.0 (quality of lead)
- Sentiment: -1.0 to 1.0 (caller sentiment)
- Qualified: boolean (high enough to route)

**Step 5: Route Decision**
- Query highest bidder for classified lead category
- Apply category premium
- Check quota availability
- Return to telephony engine

```javascript
// Simplified routing logic pseudo-code
async function routeCall(inboundNumber, callerId, metadata) {
  // 1. AI screening (parallelizable, cacheable)
  const aiResults = await aiService.screen({
    inboundNumber,
    callerId,
    metadata
  });
  
  // 2. Get classified category
  const category = await prisma.leadCategory.findUnique(aiResults.leadCategoryId);
  
  // 3. Find best bid for this category
  const bestBid = await prisma.bid.findFirst({
    where: {
      categoryId: category.id,
      status: 'ACCEPTED',
      user: { isActive: true }
    },
    orderBy: { amountCents: 'desc' },
    take: 1
  });
  
  // 4. Check quota
  if (bestBid && bestBid.quota && bestBid.usedQuota >= bestBid.quota) {
    // Fallback to next best
    return fallbackRouting(inboundNumber);
  }
  
  // 5. Return routing decision
  return {
    buyerId: bestBid.userId,
    destination: bestBid.user.billingProfile.stripeAccId,
    effectiveBid: bestBid.amountCents + category.premium,
    aiResults
  };
}
```

### 5.2 Per-Category Bidding Flow

**Buyer Creates Bid:**
1. Select lead category (e.g., "Personal Auto")
2. Set bid amount (¢/call or ¢/minute)
3. Set monthly quota (max calls)
4. System checks available credit
5. Bid status = `PENDING`

**AI Classifies Lead:**
1. AI determines lead category during screening
2. Query active bids for that category
3. Apply category premium (base bid + premium rate)
4. Check quota remaining
5. Select highest bidder
6. Route call to winner

**Payment Processing:**
1. Call connects → deduct credit from buyer (pre-payment)
2. Call ends → finalize charge (prorated if dropped)
3. Platform fee calculated (10-15% based on volume)
4. Seller credited (same-day payout available)

### 5.3 Call Completion & Lead Storage

**Scenario: Call connects, drops after 30 seconds**

1. **AI already captured full lead data** during screening
2. **LeadEnrichment record created:**
   - `structuredData`: complete buyer info, needs, budget, timeframe
   - `transcript`: partial/full call transcript
   - `leadCategory`: classified category
   - `score`: quality score
3. **CallLog updated:**
   - `status = DROPPED`
   - `costCents`: prorated for 30 seconds
   - `revenueCents`: prorated revenue
4. **Buyer credited:** partial call duration (prorated refund)
5. **Lead saved:** available in marketplace for future sales

**Scenario: Call never connects (no answer)**
1. **AI screening completed** before routing
2. **LeadEnrichment stored** with initial data from screening
3. **No charge** to buyer (no connection)
4. **Lead available:** can be sold later at discount

### 5.4 Credit Flow

| Event | Action | Database Change |
|-------|--------|----------------|
| **Funding** | Stripe Checkout → `StripeCharge` → `User.creditBalanceCents += amount` | `creditBalanceCents` updated |
| **Call Connect** | Deduct bid amount immediately | `creditBalanceCents -= bidAmount` |
| **Call Complete** | Finalize charge (prorated) | `creditBalanceCents -= prorated` |
| **Refund** | If call fails | `creditBalanceCents += refund` |
| **Payout** | Batch payout via Stripe | `StripePayout` record created |

**Credit Balance Formula:**
```javascript
currentBalance = initialBalance
  + (sum of all successful charges)
  - (sum of all deductions for connected calls)
  + (sum of all refunds for failed calls)
```

---

## 6. Performance & Scaling Strategy

| Requirement | Strategy | Expected Performance |
|-------------|----------|-------------------|
| **<50ms routing** | Redis cache per inbound number → pre-compute best bid | <50ms p99 |
| **Real-Time STT** | WebRTC streaming → STT service with streaming responses | <100ms latency |
| **AI Scoring** | LLM inference with caching for similar callers | <200ms p95 |
| **Thousands concurrent calls** | Stateless API servers, read replicas for analytics | Scales horizontally |
| **Same-day payouts** | Stripe Instant Payout API (connected accounts) | <1 minute |
| **Fault tolerance** | AI service fallback to rule-based classification | 99.9% uptime |

**Redis Cache Structure:**
```redis
# Key: routing:{inboundNumber}:{leadCategoryId}
# Value: {"buyerId": "uuid", "effectiveBid": 500, "quota": 1000, "lastUpdated": 1709658000}
# TTL: 10 seconds

# Key: ai:{callerId}:{leadCategoryId}
# Value: {"leadCategory": "uuid", "score": 0.85, "structuredData": {...}}
# TTL: 60 seconds
```

**AI Service Architecture:**
```
┌─────────────────────────┐     ┌──────────────────────────┐
│  Inbound Call           │     │  AI Screening Service    │
└─────────────────────────┘     └──────────────────────────┘
              │                             │
              ▼                             ▼
┌─────────────────────────┐     ┌──────────────────────────┐
│  STT Service            │     │  Intent Classifier       │
│  (Whisper AI)           │     │  (LLM-based)             │
└─────────────────────────┘     └──────────────────────────┘
              │                             │
              ▼                             ▼
┌─────────────────────────┐     ┌──────────────────────────┐
│  Data Extractor         │     │  Lead Scorer             │
└─────────────────────────┘     └──────────────────────────┘
```

---

## 7. Security & Compliance

| Concern | Mitigation |
|---------|------------|
| **Credit/debit race conditions** | Database transaction with `SELECT FOR UPDATE` on `User.creditBalanceCents` |
| **Stripe webhook spoofing** | Verify Stripe signature header (HMAC SHA256) |
| **Data at rest** | PostgreSQL encryption with TDE |
| **PII in transcripts** | Redact PII in analytics logs; encrypt at rest |
| **GDPR compliance** | 90-day retention for call logs; data deletion API |
| **HIPAA compliance** | For health-related categories: separate encryption, BAA with AI provider |
| **AI inference security** | LLM calls through encrypted tunnel; audit logs for all AI queries |
| **API security** | JWT signed with RS256; rate limiting; secrets in Vault |

---

## 8. Deployment & Operations

### 8.1 Infrastructure
- **Container orchestration:** Kubernetes or similar
- **API Gateway:** Rate limiting, auth, logging
- **Database:** PostgreSQL with read replicas
- **Cache:** Redis cluster (high availability)
- **AI Service:** Auto-scaled microservice
- **Storage:** S3 for transcripts and recordings

### 8.2 Monitoring & Alerting
- **Metrics:** Prometheus + Grafana
- **Logs:** ELK stack
- **Alerts:** Slack notifications for:
  - AI service failures
  - Low credit balances
  - Routing errors
  - Payout failures

### 8.3 Backup & Recovery
- **Daily PostgreSQL dumps** to S3
- **Weekly full backups** with 30-day retention
- **Point-in-time recovery** enabled

---

## 9. Summary of Updates

| Feature | Original | Updated |
|---------|----------|---------|
| **Bidding** | Per-campaign, static bid | Per-category, dynamic, with quotas |
| **Routing** | Number → Campaign → Bid | Number → AI Screen → Category → Bid |
| **Lead Data** | Minimal (duration, status) | Full structured package (intent, budget, transcript) |
| **AI Pre-Screening** | Not present | Real-time STT, intent classification, scoring |
| **Lead Retention** | Only connected calls | All leads stored (including dropped calls) |
| **API** | Basic routing | AI-driven routing with enriched responses |
| **Category System** | Flat categories | Hierarchical categories with premiums |

---

## 10. Next Steps for Development

1. **Generate Prisma client** and run migrations
2. **Build core API routes** for routing & call completion
3. **Implement Redis cache** logic for routing lookups
4. **Integrate Stripe SDK** for payments & payouts
5. **Set up AI screening service** (STT + Intent Classifier)
6. **Develop per-category bidding logic** with quota enforcement
7. **Set up monitoring** for AI latency and classification accuracy
8. **Configure fallback** for AI service outages
9. **Create admin dashboard** for category management
10. **Test scaling** with load testing

---

## 11. Deliverables

1. **Prisma Schema** (complete, ready to deploy)
2. **OpenAPI Specification** (auto-generated from code)
3. **AI Service Architecture** (deployment & scaling)
4. **API Response Examples** (requests, responses)
5. **Deployment Scripts** (Dockerfile, Kubernetes manifests)
6. **Test Plan** (unit tests, integration tests, load tests)

---

## 12. Conclusion

Ringo's backend is a high-performance, highly-available system built on PostgreSQL with Prisma ORM, Redis for sub-50ms routing, Stripe for payments, and an AI service for pre-call qualification. The database schema supports all core entities with careful attention to audit, scalability, and security. The API surface is clean, role-based, and designed for rapid integration. This architecture satisfies all stated constraints: fast routing, credit management, same-day payouts, and a foundation for AI-driven call qualification with category-based bidding.

**Estimated Development Timeline:**
- Weeks 1-2: Database setup, basic API scaffolding
- Weeks 3-4: Routing logic, Redis caching integration
- Weeks 5-6: AI screening service development
- Weeks 7-8: Payment integration, testing
- Week 9: Load testing, optimization
- Week 10: Production deployment, monitoring setup

**Total: ~10 weeks to MVP**

---

**Document End**
*Last updated: 2026-03-05 13:25 MST*
