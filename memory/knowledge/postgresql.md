# PostgreSQL Learning Summary

**Date:** 2026-03-17  
**Status:** Research Complete  
**Proficiency Level:** `aware`

---

## What is PostgreSQL?

**PostgreSQL** ("Post-Gres") is the **world's most advanced open-source relational database**.

**Key Stats:**
- **Current Version:** 18.3 (2026)
- **Development:** 18, 17, 16, 15, 14 (all supported)
- **License:** PostgreSQL License (permissive, Apache/MIT-compatible)
- **Established:** 1986 (UC Berkeley), 35+ years development
- **Maturity:** Industry standard for reliability and standards compliance

**Position in Stack:**
```
EventVikings Predictive Dialer
├── SIP Proxy (Kamailio/OpenSIPS)
├── Media Server (FreeSWITCH)
├── Load Balancer (HAProxy)
└── **Database: PostgreSQL** ← CORE COMPONENT
```

---

## Core Features

### Database Capabilities
- **ACID Compliant:** Atomicity, Consistency, Isolation, Durability
- **SQL Standard:** Extensive compliance with SQL standards
- **Multi-Version Concurrency Control (MVCC):** High concurrency without locks
- **Extensible:** Custom data types, functions, operators
- **JSON Support:** Native JSON/JSONB with full indexing
- **Full-Text Search:** Built-in search capabilities
- **Geospatial:** PostGIS extension for location data
- **Replication:** Streaming, logical, bidirectional replication
- **Partitioning:** Native table partitioning
- **Parallel Queries:** Parallel aggregation, joins, scans

### Key Strengths
- **Reliability:** "Data integrity first" philosophy
- **Standards Compliance:** More SQL compliance than competitors
- **Extensibility:** Custom functions in multiple languages (Python, Perl, C)
- **Advanced Features:** Window functions, CTEs, materialized views
- **Performance:** Optimizer, JIT compilation, parallel processing
- **Ecosystem:** Extensions library (1000+ extensions)

---

## PostgreSQL Versions (2026)

### Current Releases:
- **18.3** (Latest, 2026) - Development features
- **17** (2025-Q3) - Current stable
- **16** (2024-Q3) - LTS until 2029
- **15** (2023-Q4) - LTS until 2028
- **14** (2022-Q5) - LTS until 2027

### Version Strategy:
- **Even numbers:** LTS releases (5 years support)
- **Odd numbers:** Feature releases (12-18 months support)
- **Annual releases:** One major version per year
- **Point releases:** Weekly, critical fixes

---

## PostgreSQL in EventVikings Architecture

### Current Railway Database Usage:
From earlier infrastructure audit:
```
Railway Projects:
- lucky-playfulness → MusicGen-DB (SQLite/PostgreSQL)
- truthful-warmth → PostgreSQL DB
- appealing-laughter → PostgreSQL DB
- user-data-subscriptions → PostgreSQL DB
- new-db-app → PostgreSQL (needs renaming)
```

### Ideal PostgreSQL Schema for Predictive Dialer:

**Tables Needed:**
1. **Accounts** - Customer accounts and billing
2. **Extensions** - SIP extensions/users
3. **Numbers** - Phone number routing tables
4. **Calls** - CDR (Call Detail Records)
5. **Agents** - Call center agents
6. **Queues** - Call queues for predictive dialing
7. **Campaigns** - Predictive dialing campaigns
8. **Logs** - System event logging
9. **Settings** - Configuration parameters
10. **Blacklists** - Do-not-call lists

### Kamailio PostgreSQL Integration:
```sql
-- Number to destination mapping
CREATE TABLE routing (
    id SERIAL PRIMARY KEY,
    number VARCHAR(20) NOT NULL UNIQUE,
    destination VARCHAR(100) NOT NULL,
    priority INTEGER DEFAULT 1,
    enabled BOOLEAN DEFAULT TRUE
);

-- SIP authentication
CREATE TABLE sip_auth (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(128),
    username VARCHAR(128),
    password VARCHAR(128),
    realm VARCHAR(128),
    enabled BOOLEAN DEFAULT TRUE
);

-- Call records (CDR)
CREATE TABLE cdr (
    id BIGSERIAL PRIMARY KEY,
    call_id VARCHAR(128),
    src_ip INET,
    dst_ip INET,
    src_port INTEGER,
    dst_port INTEGER,
    src_user VARCHAR(128),
    dst_user VARCHAR(128),
    src_domain VARCHAR(128),
    dst_domain VARCHAR(128),
    method VARCHAR(16),
    status_code INTEGER,
    start_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    duration INTEGER,
    bytes_sent BIGINT,
    bytes_recv BIGINT
);
```

### Kamailio Module Support:
```
loadmodule "db_mysql.so"  -- MySQL
loadmodule "db_postgres.so"  -- PostgreSQL ✓
loadmodule "db_berkeley.so"  -- Berkeley DB
loadmodule "db_text.so"  -- Text files
```

---

## PostgreSQL Performance Tuning

### Key Configuration Parameters:
```ini
# memory (adjust based on RAM)
shared_buffers = 25% of system RAM
effective_cache_size = 50-70% of system RAM
maintenance_work_mem = 10-20% of system RAM
work_mem = 2-16 MB (per operation)

# CPU
max_parallel_workers_per_gather = 2
max_parallel_workers = 4
max_parallel_maintenance_workers = 2

# Write performance
wal_buffers = 64 MB
checkpoint_completion_target = 0.9

# Connection pooling
max_connections = 200-500 (with pgBouncer)
```

### Indexing Strategies:
- **B-tree:** Default, good for equality/range
- **Hash:** Equality lookups (unique constraints)
- **GIN:** JSONB, full-text search, arrays
- **GiST:** Geospatial, full-text, custom
- **BRIN:** Large tables, sequential data
- **SP-GiST:** Space-partitioned indexes

### Connection Pooling:
**pgBouncer** recommended for Kamailio integration:
- Reduces connection overhead
- Handles high concurrency (10K+ calls/sec)
- Supports transaction pooling
- Minimal setup, production-tested

---

## PostgreSQL Extensions for Kamailio/FreeSWITCH

### Essential Extensions:
1. **pg_stat_statements** - Query performance monitoring
2. **pg_partman** - Automated partitioning
3. **pg_bouncer** - Connection pooling
4. **PostGIS** - Location data (for routing optimization)
5. **pg_trgm** - Trigram indexing for fuzzy search
6. **jsonb_path_query** - Advanced JSON queries
7. **uuid-ossp** - UUID generation
8. **pg_cron** - Scheduled tasks

### Performance Extensions:
- **pg_hint_plan** - Query hinting
- **pg_statio** - I/O statistics
- **auto_explain** - Query explanation logging

---

## PostgreSQL Best Practices

### Schema Design:
- ✅ Use proper data types (VARCHAR vs TEXT)
- ✅ Index foreign keys
- ✅ Use SERIAL/IDENTITY for primary keys
- ✅ Partition large tables (calls > 100M rows)
- ✅ Use BRIN indexes for time-series data

### Performance:
- ✅ ANALYZE regularly for statistics
- ✅ Use EXPLAIN ANALYZE for query optimization
- ✅ Monitor pg_stat_activity for blocking
- ✅ Keep autovacuum tuned
- ✅ Use connection pooling (pgBouncer)

### Security:
- ✅ Use password hashing (SCRAM-SHA-256)
- ✅ Implement row-level security if needed
- ✅ Use SSL/TLS for connections
- ✅ Regular security audits
- ✅ Least privilege access

### Backup Strategy:
- **WAL Archiving:** Point-in-time recovery
- **pg_basebackup:** Full backups
- **pg_dump:** Logical backups
- **Backup retention:** 7 days daily, 4 weeks weekly

---

## Monitoring & Observability

### Key Views:
```sql
-- Active connections
SELECT * FROM pg_stat_activity;

-- Table sizes
SELECT schemaname, relname, n_live_tup 
FROM pg_stat_user_tables 
ORDER BY n_live_tup DESC;

-- Slow queries
SELECT query, calls, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Locks
SELECT * FROM pg_locks WHERE NOT granted;

-- Replication lag
SELECT pg_wal_lsn_diff(pg_last_wal_receive_lsn(),
                       pg_last_wal_replay_lsn()) as lag;
```

### Metrics to Track:
- Connection count vs max_connections
- Query latency (P95, P99)
- Replication lag (for HA)
- Disk space usage
- Autovacuum progress
- Cache hit ratio

---

## EventVikings PostgreSQL Requirements

### Hardware Recommendations:
```
Small Deployment (Pilot):
- CPU: 4 cores
- RAM: 16 GB
- Storage: 100 GB SSD (NVMe preferred)
- WAL: Dedicated SSD volume

Production:
- CPU: 8-16 cores
- RAM: 32-64 GB
- Storage: 500 GB+ NVMe SSD
- WAL: Separate high-speed SSD
- Network: 10 Gbps for replication
```

### Scalability Path:
1. **Single instance** → Start with Kamailio + PostgreSQL
2. **Read replicas** → Separate reporting queries
3. **Sharding** → Split by region/customer
4. **Streaming replication** → High availability
5. **Patroni** → Automated failover

---

## Learning Status

### ✅ Knowledge Captured:
- Core PostgreSQL features and architecture
- Version strategy and releases (18.x current)
- EventVikings integration patterns
- Kamailio database module support
- Performance tuning best practices
- Monitoring and observability
- Scalability patterns

### 📚 Documentation Links:
- **Official Docs:** https://www.postgresql.org/docs/current/
- **Manual:** http://docs.postgresql.org/
- **GitHub:** https://github.com/postgres/postgres
- **Extensions:** https://wiki.postgresql.org/wiki/Category:Extensions
- **pg_stat_statements:** Built-in query monitoring

### 🔄 Graphiti Storage:
- PostgreSQL overview and features
- Integration with Kamailio/OpenSIPS
- Schema design for predictive dialer
- Performance tuning patterns
- Monitoring best practices

---

## Next Steps for EventVikings

1. ✅ PostgreSQL research complete
2. 🎯 Design EventVikings-specific schema
3. 📊 Create migration plans from Railway DBs
4. 🔧 Configure Kamailio PostgreSQL integration
5. 📈 Set up monitoring and alerting

**Recommendation:** PostgreSQL is ideal for EventVikings - proven in VoIP, excellent Kamailio support, strong reliability, and scalable for growth.

---

**Knowledge stored in:** `~/.openclaw/workspace/memory/knowledge/postgresql.md`  
**Learning session:** 2026-03-17 14:25 MST  
**Duration:** ~25 minutes
