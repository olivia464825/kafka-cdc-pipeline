# CDC Pipeline Usage Guide

## File Organization

### Production Files

```
Core Files (Production):
├── producer.py                      # Producer with connection pool
├── consumer_final.py                # Production Consumer
├── employee.py                      # Data model
├── setup_db.sql                     # Database setup
├── setup_db_with_idempotency.sql    # Idempotency table
├── docker-compose.yml               # Service configuration
└── docker-compose.monitoring.yml    # Monitoring stack (optional)
```

### Reference Files (Learning)

```
Reference Implementations (Study):
├── consumer.py                      # Basic version
├── consumer_with_dlq.py             # DLQ example
├── consumer_idempotent.py           # Idempotency example
└── ARCHITECTURE_IMPROVEMENTS.md     # Architecture guide
```

## Quick Start

### 1. Start Services

```bash
# Start Kafka + PostgreSQL
docker-compose up -d

# Wait for services to be ready
sleep 15
```

### 2. Setup Databases

```bash
# Option A: Basic setup (no idempotency)
docker exec -i proj2-db_source-1 psql -U postgres < setup_db.sql
docker exec proj2-db_dst-1 psql -U postgres -c "
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    dob DATE,
    city VARCHAR(100),
    salary INT
);"

# Option B: Full setup (recommended, includes idempotency)
docker exec -i proj2-db_source-1 psql -U postgres < setup_db.sql
docker exec -i proj2-db_dst-1 psql -U postgres < setup_db_with_idempotency.sql
```

### 3. Run CDC Pipeline

```bash
# Terminal 1: Start Producer
python producer.py

# Terminal 2: Start Consumer (production version)
python consumer_final.py
```

## Consumer Configuration

### consumer_final.py Parameters

```python
consumer = ProductionCDCConsumer(
    host="localhost",              # Kafka host
    port="29092",                  # Kafka port
    group_id='my_consumer_group',  # Consumer Group ID
    db_host="localhost",           # Destination DB host
    db_port="5433",                # Destination DB port
    enable_dlq=True,               # Enable DLQ (recommended)
    enable_idempotency=True        # Enable idempotency (recommended)
)
```

### Feature Toggles

| Parameter | Default | Description | Production |
|-----------|---------|-------------|------------|
| `enable_dlq` | `True` | Dead Letter Queue for error isolation | Required |
| `enable_idempotency` | `True` | Prevent duplicate processing | Required |

## Testing

### Test INSERT
```bash
docker exec proj2-db_source-1 psql -U postgres -c "
INSERT INTO employees (first_name, last_name, dob, city, salary)
VALUES ('John', 'Doe', '1990-01-01', 'NYC', 80000);
"
```

### Test UPDATE
```bash
docker exec proj2-db_source-1 psql -U postgres -c "
UPDATE employees SET salary = 90000 WHERE emp_id = 1;
"
```

### Test DELETE
```bash
docker exec proj2-db_source-1 psql -U postgres -c "
DELETE FROM employees WHERE emp_id = 1;
"
```

### Verify Synchronization
```bash
# Source database
docker exec proj2-db_source-1 psql -U postgres -c "
SELECT * FROM employees ORDER BY emp_id;
"

# Destination database
docker exec proj2-db_dst-1 psql -U postgres -c "
SELECT * FROM employees ORDER BY emp_id;
"

# Should be identical
```

## Monitoring

### Start Monitoring Stack (Optional)
```bash
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d

# Access Grafana
open http://localhost:3000  # Default: admin/admin

# Access Prometheus
open http://localhost:9090
```

### View Statistics
Consumer automatically outputs statistics:
```
Stats: Processed=100, Failed=0, Duplicates=5, DLQ=0
```

## Troubleshooting

### View DLQ Messages
```bash
docker exec proj2-kafka-1 kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic bf_employee_cdc_dlq \
  --from-beginning
```

### Reset Consumer Group (Re-consume)
```bash
# Stop consumer first
# Then reset offset
docker exec proj2-kafka-1 kafka-consumer-groups \
  --bootstrap-server localhost:9092 \
  --group production_cdc_consumer \
  --reset-offsets --to-earliest \
  --topic bf_employee_cdc \
  --execute
```

### View Idempotency Tracking
```bash
docker exec proj2-db_dst-1 psql -U postgres -c "
SELECT action_id, emp_id, action, processed_at
FROM processed_events
ORDER BY action_id DESC
LIMIT 10;
"
```

## Version Comparison

### Which Consumer Should I Use?

| Scenario | File | Reason |
|----------|------|--------|
| Production | `consumer_final.py` | All features included |
| Development | `consumer_final.py` | Same recommendation |
| Learn DLQ | `consumer_with_dlq.py` | Educational reference |
| Learn Idempotency | `consumer_idempotent.py` | Educational reference |
| Basic Learning | `consumer.py` | Minimal example |

**Recommendation**: Use `consumer_final.py` directly - it's the most complete version.

## Best Practices

### Production Environment Checklist

Required:
- [ ] Use `consumer_final.py`
- [ ] Enable DLQ (`enable_dlq=True`)
- [ ] Enable idempotency (`enable_idempotency=True`)
- [ ] Setup `processed_events` table
- [ ] Configure monitoring (Prometheus + Grafana)
- [ ] Setup alerting rules

Recommended:
- [ ] Use configuration files (don't hardcode credentials)
- [ ] Set appropriate log levels
- [ ] Regular DLQ cleanup
- [ ] Database backups

## Additional Resources

View detailed architecture improvements:
```bash
cat ARCHITECTURE_IMPROVEMENTS.md
```

## Common Questions

### Q: Why multiple consumer files?
**A**: Other consumer files are educational references showing individual features. **Production environments should use `consumer_final.py`**.

### Q: What if I don't need idempotency?
**A**: Set `enable_idempotency=False`, or don't create the `processed_events` table.

### Q: How to handle DLQ messages?
**A**:
1. View DLQ to identify failure reasons
2. Fix the issue (data or code)
3. Manually replay DLQ messages

### Q: Performance?
**A**:
- Connection pool: ~100x improvement
- Batch processing: Statistics every 10 messages
- Transactions: Atomicity with maximum throughput

## Simple Version

```bash
# 1. Start services
docker-compose up -d

# 2. Setup databases
docker exec -i proj2-db_source-1 psql -U postgres < setup_db.sql
docker exec -i proj2-db_dst-1 psql -U postgres < setup_db_with_idempotency.sql

# 3. Run
python producer.py &
python consumer_final.py
```

That's it!
