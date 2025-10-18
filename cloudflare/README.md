# Cloudflare Setup Guide

This directory contains configuration files for Cloudflare services (D1 database and KV storage).

## Prerequisites

1. Install Wrangler CLI:
```bash
npm install -g wrangler
```

2. Login to Cloudflare:
```bash
wrangler login
```

## Setup D1 Database

1. Create a new D1 database:
```bash
wrangler d1 create unfreeze-db
```

2. Copy the `database_id` from the output and update `wrangler.toml`

3. Initialize the database schema:
```bash
wrangler d1 execute unfreeze-db --file=./schema.sql
```

4. Test queries locally:
```bash
wrangler d1 execute unfreeze-db --command="SELECT * FROM users"
```

## Setup KV Namespace

1. Create a new KV namespace:
```bash
wrangler kv:namespace create "KV"
```

2. Copy the `id` from the output and update `wrangler.toml`

3. Test KV locally:
```bash
wrangler kv:key put --namespace-id=YOUR_ID "test" "Hello World"
wrangler kv:key get --namespace-id=YOUR_ID "test"
```

## Get API Credentials

1. Go to Cloudflare Dashboard → Profile → API Tokens

2. Create a token with these permissions:
   - Account > D1 > Edit
   - Account > Workers KV Storage > Edit

3. Copy your Account ID from the dashboard

4. Add to your backend `.env` file:
```env
CLOUDFLARE_ACCOUNT_ID=your_account_id
CLOUDFLARE_API_TOKEN=your_api_token
CLOUDFLARE_D1_DATABASE_ID=your_database_id
CLOUDFLARE_KV_NAMESPACE_ID=your_kv_namespace_id
```

## Database Migrations

To update the schema:

1. Edit `schema.sql` with your changes

2. Execute the migration:
```bash
wrangler d1 execute unfreeze-db --file=./schema.sql
```

## Testing Locally

You can test D1 queries without deploying:

```bash
# Execute SQL
wrangler d1 execute unfreeze-db --command="SELECT * FROM users LIMIT 5"

# Run from file
wrangler d1 execute unfreeze-db --file=./test-queries.sql
```

## Useful Commands

```bash
# List all D1 databases
wrangler d1 list

# List all KV namespaces
wrangler kv:namespace list

# Export D1 data
wrangler d1 export unfreeze-db --output=backup.sql

# Import D1 data
wrangler d1 execute unfreeze-db --file=backup.sql
```

## Resources

- [Cloudflare D1 Docs](https://developers.cloudflare.com/d1/)
- [Cloudflare KV Docs](https://developers.cloudflare.com/kv/)
- [Wrangler CLI Docs](https://developers.cloudflare.com/workers/wrangler/)

