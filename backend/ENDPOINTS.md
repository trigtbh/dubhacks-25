# 🚀 API Endpoints Reference

> **Consolidated documentation** for all HTTP endpoints in the Unfreeze backend API. Use this as your single source of truth for testing and integration.

## 📋 Table of Contents

- [Server Configuration](#server-configuration)
- [Prerequisites](#prerequisites)
- [General Endpoints](#general-endpoints)
- [Application Routes](#application-routes)
- [Vectorization & Clustering](#vectorization--clustering)
- [Cloudflare Services](#cloudflare-services)
  - [D1 Database](#d1-database)
  - [KV Storage](#kv-storage)
  - [R2 Object Storage](#r2-object-storage)
- [Troubleshooting](#troubleshooting)

---

## 🖥️ Server Configuration

**Base URL:** `http://localhost:8000`

*Defaults from `app/config.py`: `api_host=0.0.0.0`, `api_port=8000`*

---

## ⚙️ Prerequisites

### Environment Variables

Cloudflare integration requires the following environment variables in `backend/.env`:

| Variable | Service | Required |
|----------|---------|----------|
| `CLOUDFLARE_ACCOUNT_ID` | All | ✅ |
| `CLOUDFLARE_API_TOKEN` | All | ✅ |
| `CLOUDFLARE_D1_DATABASE_ID` | D1 Database | ✅ |
| `CLOUDFLARE_KV_NAMESPACE_ID` | KV Storage | ✅ |
| `CLOUDFLARE_R2_ACCOUNT_ID` | R2 Storage | ✅ |
| `CLOUDFLARE_R2_ACCESS_KEY_ID` | R2 Storage | ✅ |
| `CLOUDFLARE_R2_SECRET_ACCESS_KEY` | R2 Storage | ✅ |
| `CLOUDFLARE_R2_BUCKET_NAME` | R2 Storage | ✅ |

### Dependencies

- **Pillow** is required for the R2 test endpoint (added to `requirements.txt`)

---

## 🌐 General Endpoints

### `GET /`

**Health check endpoint**

- **Request:** None
- **Response:** JSON with service status

### `GET /health`

**Detailed health check with service status**

- **Request:** None
- **Response:** JSON with platform info and Cloudflare configuration status

---

## 📱 Application Routes

### `POST /unfreeze`

**Process text input (placeholder endpoint)**

- **Request:**
  ```json
  {
    "text": "input text to process"
  }
  ```
- **Response (200):**
  ```json
  {
    "message": "Successfully unfroze: input text to process",
    "input": "input text to process",
    "timestamp": "2025-10-18T12:00:00.000Z"
  }
  ```
- **Errors:** `400` if text is empty

### `GET /status`

**Simple service status**

- **Request:** None
- **Response:** JSON with available endpoints and timestamp

---

## 🤖 Vectorization & Clustering

**Base Path:** `/api/v1/users`

### Data Models

#### `UserAttributes`

```json
{
  "uuid": "string",
  "specialty": "skill1, skill2",
  "fields": "field1, field2",
  "interests_and_hobbies": "interest1, interest2, hobby1",
  "vibe": "personality description",
  "comfort": ["comfort1", "comfort2"],
  "availability": "schedule description"
}
```

### `POST /api/v1/users/vectorize`

**Convert user attributes to TF-IDF vectors**

- **Request:**
  ```json
  {
    "users": [
      {
        "uuid": "user123",
        "specialty": "Python, JavaScript",
        "fields": "Software Engineering, Web",
        "interests_and_hobbies": "AI, Web Development, Reading",
        "vibe": "Creative and analytical",
        "comfort": ["Remote work", "Flexible hours"],
        "availability": "Weekends and evenings",
        "handle": "@user123"
      }
    ]
  }
  ```
- **Response:**
  ```json
  {
    "vectorized_users": [
      {
        "uuid": "user123",
        "vector": [0.1, 0.2, 0.0, ...],
        "attributes": { /* UserAttributes */ },
        "vector_dimension": 100
      }
    ],
    "vector_dimension": 100,
    "timestamp": "2025-10-18T12:00:00.000Z"
  }
  ```

### `POST /api/v1/users/cluster`

**Cluster users using K-Means algorithm**

- **Request:**
  ```json
  {
    "users": [ /* UserAttributes array */ ],
    "num_clusters": 3,
    "min_interest_overlap": 0.0
  }
  ```
- **Response:**
  ```json
  {
    "clusters": [
      {
        "cluster_id": 0,
        "uuids": ["user1", "user2"],
        "size": 2,
        "common_interests": ["AI", "Python"],
        "similarity_score": 0.75
      }
    ],
    "num_clusters": 3,
    "total_users": 10,
    "clustering_method": "K-Means with TF-IDF vectorization",
    "timestamp": "2025-10-18T12:00:00.000Z"
  }
  ```

### `POST /api/v1/users/find-similar`

**Find most similar users to a reference user**

- **Request:**
  ```json
  {
    "user": { /* UserAttributes */ },
    "all_users": [ /* UserAttributes array */ ],
    "top_k": 5
  }
  ```
- **Response:**
  ```json
  {
    "reference_uuid": "user123",
    "similar_users": [
      {
        "uuid": "user456",
        "similarity_score": 0.85,
        "shared_interests": ["AI", "Python"]
      }
    ],
    "timestamp": "2025-10-18T12:00:00.000Z"
  }
  ```

### `GET /api/v1/users/vectorize/status`

**Vectorization service status**

- **Request:** None
- **Response:** JSON with service capabilities and timestamp

---

## ☁️ Cloudflare Services

**Base Path:** `/cloudflare`

---

## 🗄️ D1 Database

### `GET /cloudflare/d1/status`

**Check D1 database connectivity**

- **Response:**
  ```json
  {
    "configured": true,
    "status": "connected",
    "message": "Cloudflare D1 is properly configured and connected",
    "test_result": { /* query result */ }
  }
  ```

### `POST /cloudflare/d1/query`

**Execute single SQL query**

- **Request:**
  ```json
  {
    "sql": "SELECT * FROM users WHERE id = ?",
    "params": [1]
  }
  ```
- **Response:**
  ```json
  {
    "success": true,
    "data": { /* query result */ }
  }
  ```
- **Note:** Requires D1 configuration

### `POST /cloudflare/d1/batch`

**Execute multiple SQL queries**

- **Request:**
  ```json
  {
    "queries": [
      {
        "sql": "INSERT INTO users (name) VALUES (?)",
        "params": ["John"]
      },
      {
        "sql": "SELECT * FROM users",
        "params": []
      }
    ]
  }
  ```
- **Response:**
  ```json
  {
    "success": true,
    "data": { /* batch result */ }
  }
  ```

---

## 🔑 KV Storage

### `GET /cloudflare/kv/status`

**Check KV storage status**

- **Response:**
  ```json
  {
    "configured": true,
    "status": "ready",
    "message": "Cloudflare KV is properly configured"
  }
  ```

### `GET /cloudflare/kv/{key}`

**Retrieve value by key**

- **Path Parameters:** `key` (string)
- **Response:**
  ```json
  {
    "key": "mykey",
    "value": "myvalue"
  }
  ```
- **Errors:** `404` if key not found

### `PUT /cloudflare/kv`

**Store key-value pair**

- **Request:**
  ```json
  {
    "key": "mykey",
    "value": "myvalue",
    "expiration_ttl": 3600
  }
  ```
- **Response:**
  ```json
  {
    "success": true,
    "key": "mykey"
  }
  ```

### `DELETE /cloudflare/kv/{key}`

**Delete key-value pair**

- **Path Parameters:** `key` (string)
- **Response:**
  ```json
  {
    "success": true,
    "key": "mykey"
  }
  ```

### `GET /cloudflare/kv/list/keys`

**List keys in namespace**

- **Query Parameters:**
  - `prefix` (optional): Filter by key prefix
  - `limit` (optional): Max keys to return (default: 100)
- **Response:**
  ```json
  {
    "keys": ["key1", "key2", "key3"],
    "count": 3
  }
  ```

---

## 📦 R2 Object Storage

*S3-compatible object storage*

**Prerequisites:** R2 credentials and bucket configured in environment

### `GET /cloudflare/r2/status`

**Check R2 configuration**

- **Response:**
  ```json
  {
    "configured": true,
    "status": "ready",
    "message": "Cloudflare R2 is properly configured"
  }
  ```

### `POST /cloudflare/r2/presigned-upload-url`

**Generate presigned upload URL**

- **Request:**
  ```json
  {
    "key": "path/to/object.png",
    "expires_in": 3600,
    "content_type": "image/png"
  }
  ```
- **Response:**
  ```json
  {
    "success": true,
    "url": "https://presigned-upload-url",
    "key": "path/to/object.png",
    "method": "PUT",
    "expires_in": 3600
  }
  ```

### `POST /cloudflare/r2/presigned-download-url`

**Generate presigned download URL**

- **Request:**
  ```json
  {
    "key": "path/to/object.png",
    "expires_in": 3600,
    "filename": "download.png"
  }
  ```
- **Response:**
  ```json
  {
    "success": true,
    "url": "https://presigned-download-url",
    "key": "path/to/object.png",
    "method": "GET",
    "expires_in": 3600
  }
  ```

### `POST /cloudflare/r2/upload`

**Upload file through backend**

- **Query Parameters:** `key` (string)
- **Body:** `multipart/form-data` with `file` field
- **Response:**
  ```json
  {
    "success": true,
    "key": "path/to/object.png",
    "filename": "uploaded-file.png",
    "size": 1024
  }
  ```

### `GET /cloudflare/r2/download/{key}`

**Download file through backend**

- **Path Parameters:** `key` (supports slashes)
- **Response:** Raw file bytes with `application/octet-stream` content type

### `DELETE /cloudflare/r2/{key}`

**Delete file from R2**

- **Path Parameters:** `key` (string)
- **Response:**
  ```json
  {
    "success": true,
    "key": "path/to/object.png"
  }
  ```

### `GET /cloudflare/r2/list`

**List objects in bucket**

- **Query Parameters:**
  - `prefix` (optional): Filter by key prefix
  - `max_keys` (optional): Max objects to return (default: 100)
- **Response:**
  ```json
  {
    "success": true,
    "files": [
      {
        "Key": "object1.png",
        "Size": 1024,
        "LastModified": "2025-10-18T12:00:00Z"
      }
    ],
    "count": 1
  }
  ```

### `GET /cloudflare/r2/test`

**Full presigned URL workflow demo**

*Generates sample image → uploads via presigned URL → returns download URL*

- **Response:**
  ```json
  {
    "success": true,
    "message": "Successfully uploaded test image using presigned URL workflow",
    "workflow": {
      "step_1": "Generated sample PNG image",
      "step_2": "Obtained presigned upload URL",
      "step_3": "Uploaded image to R2 via presigned URL",
      "step_4": "Generated presigned download URL"
    },
    "key": "test-images/sample-20251018-120000.png",
    "upload_url": "https://presigned-upload-url",
    "download_url": "https://presigned-download-url",
    "image_info": {
      "format": "PNG",
      "size_bytes": 12345,
      "dimensions": "400x300",
      "generated_at": "2025-10-18T12:00:00.000Z"
    },
    "instructions": {
      "view_image": "Visit the download_url to view the uploaded image",
      "direct_link": "https://presigned-download-url"
    }
  }
  ```
- **Note:** Requires Pillow and R2 configuration

---

## 🔧 Troubleshooting

### Configuration Issues

- **Cloudflare endpoints fail:** Verify `.env` variables match the prerequisites table
- **R2 test endpoint fails:** Ensure Pillow is installed and R2 credentials are valid

### Presigned URL Issues

- **Timeouts:** Check `expires_in` value and system clock synchronization
- **Upload failures:** Verify network connectivity and R2 bucket permissions
- **Download failures:** Ensure the object key exists and URL hasn't expired

### General Tips

- All timestamps are in ISO 8601 format
- Error responses include detailed error messages
- Use the `/health` endpoint to check service status
- Cloudflare services require proper API tokens and account setup

---

*Generated from `backend/app/api/*` and `backend/app/main.py` source code*