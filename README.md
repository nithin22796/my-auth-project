## Migration Handling

# Create Migration
```bash
alembic revision --autogenerate -m "<MIGRATION CHANGE>"
```

# Review migration
```bash
ls -la alembic/versions/
```

# Apply migration
```bash
alembic upgrade head
```

## Common Migration commands

# Generate migration from model changes
alembic revision --autogenerate -m "Description of change"

# Create empty migration (for manual data transformations)
alembic revision -m "Description"

# Apply all pending migrations
alembic upgrade head

# Apply specific migration
alembic upgrade abc123  # revision ID

# Rollback last migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade abc123

# Rollback all migrations
alembic downgrade base

# Show current version
alembic current

# Show migration history
alembic history

# Show SQL without executing
alembic upgrade head --sql