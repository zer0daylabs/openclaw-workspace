# MusicGen API Documentation

**Version:** 1.0  
**Last Updated:** 2026-03-16  
**Base URL:** `https://edmmusic.studio/api`

## Overview

MusicGen provides a RESTful API for programmatic access to music generation features. This documentation covers all public endpoints for PRO and PREMIUM subscribers.

## Authentication

All API requests require authentication via NextAuth JWT tokens.

```javascript
// Include in all requests
headers: {
  'Authorization': `Bearer ${your_jwt_token}`,
  'Content-Type': 'application/json'
}
```

## Rate Limits

### By Subscription Tier

| Tier | Requests/min | Generations/day | Concurrent Jobs |
|------|----------|-------------|-- -------------|
| Starter | 60 | 25 | 1 |
| Pro | 120 | 125 | 2 |
| Premium | 300 | 500 | 5 |

### Rate Limit Headers

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1710672000
```

## API Endpoints

### Authentication Endpoints

#### POST /api/auth/register

**Register a new user account**

```javascript
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": "clx123...",
    "email": "user@example.com",
    "name": "John Doe",
    "credits": 100,
    "role": "USER",
    "createdAt": "2026-03-16T10:00:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

#### POST /api/auth/login

**Authenticate user and get JWT token**

```javascript
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": "clx123...",
    "email": "user@example.com",
    "name": "John Doe",
    "credits": 100,
    "role": "USER"
  },
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

#### POST /api/auth/forgot-password

**Request password reset**

```javascript
POST /api/auth/forgot-password
Content-Type: application/json

{
  "email": "user@example.com"
}
```

**Response (200 OK):**
```json
{
  "message": "Password reset email sent"
}
```

#### POST /api/auth/reset-password

**Reset password with token**

```javascript
POST /api/auth/reset-password
Content-Type: application/json

{
  "token": "reset_token_from_email",
  "password": "newSecurePassword123"
}
```

### Generation Endpoints

#### POST /api/generate

**Create a new music generation job**

```javascript
POST /api/generate
Content-Type: application/json
Authorization: Bearer <token>

{
  "instrument": "bass",
  "bpm": 130,
  "duration": 8,
  "structure": ["intro", "buildup", "drop", "outro"],
  "mood": "energetic",
  "genre": "edm",
  "format": "mp3"
}
```

**Request Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| instrument | string | Yes | bass, synth, drums, vocals, guitar, piano, strings, brass, percussion |
| bpm | number | Yes | 60-180 BPM |
| duration | number | Yes | 4, 8, 12, or 16 seconds |
| structure | string[] | No | Track structure elements |
| mood | string | No | Emotional descriptor |
| genre | string | No | Music genre |
| format | string | No | mp3, wav, ogg (default: mp3) |

**Response (201 Created):**
```json
{
  "id": "clx123456789",
  "status": "PENDING",
  "creditsUsed": 2,
  "estimatedCompletion": "2026-03-16T10:02:00Z"
}
```

#### GET /api/generate/:id

**Get generation status**

```javascript
GET /api/generate/clx123456789
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "id": "clx123456789",
  "status": "COMPLETED",
  "instrument": "bass",
  "bpm": 130,
  "duration": 8,
  "audioUrl": "https://blob.vercel-storage.com/generations/clx123456789.mp3",
  "creditsUsed": 2,
  "createdAt": "2026-03-16T10:00:00Z",
  "completedAt": "2026-03-16T10:01:30Z"
}
```

**Possible Status Values:**
- `PENDING` - Job queued
- `PROCESSING` - Generating audio
- `COMPLETED` - Ready for download
- `FAILED` - Generation failed (check `error` field)

#### DELETE /api/generate/:id

**Cancel pending generation**

```javascript
DELETE /api/generate/clx123456789
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "message": "Generation cancelled",
  "creditsRefunded": 2
}
```

### Library Endpoints

#### GET /api/library

**List user's saved loops**

```javascript
GET /api/library?limit=20&offset=0&sort=created_at&order=desc
Authorization: Bearer <token>
```

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| limit | number | 20 | Results per page (max 100) |
| offset | number | 0 | Pagination offset |
| sort | string | created_at | created_at, title, download_count |
| order | string | desc | asc or desc |
| favorite | boolean | false | Filter by favorites only |

**Response (200 OK):**
```json
{
  "loops": [
    {
      "id": "clx987654321",
      "title": "Bass Drop - 130 BPM",
      "instrument": "bass",
      "bpm": 130,
      "duration": 8,
      "audioUrl": "https://blob.vercel-storage.com/...",
      "format": "mp3",
      "creditsUsed": 2,
      "favorite": true,
      "downloadCount": 42,
      "createdAt": "2026-03-16T10:00:00Z"
    }
  ],
  "pagination": {
    "total": 150,
    "limit": 20,
    "offset": 0,
    "hasMore": true
  }
}
```

#### POST /api/library

**Save a generation to library**

```javascript
POST /api/library
Content-Type: application/json
Authorization: Bearer <token>

{
  "generationId": "clx123456789",
  "title": "My Favorite Bass Drop",
  "tags": ["bass", "edm", "drop"],
  "favorite": true
}
```

**Response (201 Created):**
```json
{
  "id": "clx987654321",
  "title": "My Favorite Bass Drop",
  "generationId": "clx123456789",
  "createdAt": "2026-03-16T10:05:00Z"
}
```

#### PATCH /api/library/:id

**Update saved loop**

```javascript
PATCH /api/library/clx987654321
Content-Type: application/json
Authorization: Bearer <token>

{
  "title": "Updated Bass Drop",
  "favorite": false
}
```

#### DELETE /api/library/:id

**Remove from library**

```javascript
DELETE /api/library/clx987654321
Authorization: Bearer <token>
```

#### GET /api/library/:id/download

**Download saved loop**

```javascript
GET /api/library/clx987654321/download
Authorization: Bearer <token>
```

**Response (200 OK):**
- Redirect to audio file URL or direct file download
- Increments download count

### Credit Endpoints

#### GET /api/credits

**Get current credit balance and subscription status**

```javascript
GET /api/credits
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "currentCredits": 47,
  "maxCredits": 500,
  "subscription": {
    "tier": "PRO",
    "status": "ACTIVE",
    "currentPeriodEnd": "2026-04-16T00:00:00Z",
    "trialEndsAt": null,
    "monthlyCredits": 500
  },
  "creditHistory": [
    {
      "id": "clx123",
      "amount": -2,
      "type": "GENERATION_USED",
      "description": "Generated bass loop",
      "createdAt": "2026-03-16T10:00:00Z"
    },
    {
      "id": "clx122",
      "amount": 500,
      "type": "SUBSCRIPTION_RENEWAL",
      "description": "Monthly credits for PRO plan",
      "createdAt": "2026-03-16T00:00:00Z"
    }
  ]
}
```

### Subscription Endpoints

#### GET /api/subscription

**Get current subscription details**

```javascript
GET /api/subscription
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "tier": "PRO",
  "status": "ACTIVE",
  "stripeCustomerId": "cus_123456",
  "currentPeriodStart": "2026-03-16T00:00:00Z",
  "currentPeriodEnd": "2026-04-16T00:00:00Z",
  "trialEndsAt": null,
  "cancelAtPeriodEnd": false,
  "plan": {
    "name": "Pro",
    "monthlyCredits": 500,
    "priceMonthly": 2999,
    "features": [
      "500 credits/month",
      "All instruments",
      "All export formats",
      "Advanced parameters",
      "Priority generation",
      "Priority support"
    ]
  }
}
```

#### POST /api/subscription/checkout

**Create Stripe checkout session**

```javascript
POST /api/subscription/checkout
Content-Type: application/json
Authorization: Bearer <token>

{
  "tier": "PRO"
}
```

**Request Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| tier | string | Yes | STARTER, PRO, or PREMIUM |

**Response (200 OK):**
```json
{
  "url": "https://checkout.stripe.com/pay/cs_..."
}
```

#### GET /api/subscription/portal

**Get customer portal link**

```javascript
GET /api/subscription/portal
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "url": "https://billing.stripe.com/p/..."
}
```

## Error Responses

### Standard Error Format

```json
{
  "error": {
    "code": "INSUFFICIENT_CREDITS",
    "message": "Insufficient credits for this operation",
    "details": {
      "required": 2,
      "available": 0
    }
  }
}
```

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 402 | Payment Required |
| 404 | Not Found |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

### Error Codes

| Code | Description |
|------|-------------|
| `UNAUTHORIZED` | Authentication required |
| `INVALID_TOKEN` | Expired or invalid JWT |
| `INSUFFICIENT_CREDITS` | Not enough credits |
| `RATE_LIMITED` | Too many requests |
| `INVALID_PARAMETER` | Request validation failed |
| `GENERATION_FAILED` | Audio generation error |
| `SUBSCRIPTION_REQUIRED` | Feature requires paid tier |
| `NOT_FOUND` | Resource doesn't exist |

## SDK Examples

### JavaScript/TypeScript

```javascript
import fetch from 'node-fetch';

const API_URL = 'https://edmmusic.studio/api';
const TOKEN = 'your_jwt_token';

// Generate music
async function generateMusic(params) {
  const response = await fetch(`${API_URL}/generate`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(params)
  });
  
  const data = await response.json();
  
  if (!response.ok) {
    throw new Error(data.error.message);
  }
  
  return data;
}

// Example usage
const generation = await generateMusic({
  instrument: 'bass',
  bpm: 130,
  duration: 8,
  mood: 'energetic',
  genre: 'edm'
});

console.log(`Generation created: ${generation.id}`);
```

### Python

```python
import requests

API_URL = 'https://edmmusic.studio/api'
TOKEN = 'your_jwt_token'

def generate_music(params):
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        f'{API_URL}/generate',
        headers=headers,
        json=params
    )
    
    response.raise_for_status()
    return response.json()

# Example usage
generation = generate_music({
    'instrument': 'bass',
    'bpm': 130,
    'duration': 8,
    'mood': 'energetic',
    'genre': 'edm'
})

print(f"Generation created: {generation['id']}")
```

## Webhooks

### Subscription Events

MusicGen sends webhooks for subscription events. Configure your webhook endpoint at `https://yourdomain.com/api/webhooks/musicgen`.

**Subscribed Events:**
- `generation.completed`
- `generation.failed`
- `subscription.created`
- `subscription.updated`
- `subscription.cancelled`

**Webhook Payload:**
```json
{
  "type": "generation.completed",
  "data": {
    "id": "clx123456789",
    "status": "COMPLETED",
    "audioUrl": "https://...",
    "userId": "clx987654321"
  },
  "timestamp": "2026-03-16T10:02:00Z"
}
```

**Webhook Signature:**
```http
X-MusicGen-Signature: sha256=...
X-MusicGen-Timestamp: 1710672000
```

Verify signature using webhook secret from dashboard.

## Versioning

Current API version: **1.0**

Version headers:
```http
API-Version: 1.0
```

Breaking changes will increment the major version number.

## Support

- **Documentation:** https://github.com/zer0daylabs/musicgen
- **Support Email:** support@edmmusic.studio
- **Status Page:** https://status.edmmusic.studio

---
Generated: 2026-03-16T22:18:00Z
