# FairProp API Documentation

## Overview

FairProp provides a RESTful API for fair housing compliance checking across 100+ global jurisdictions.

**Base URL**: `http://localhost:8000` (development)

**API Version**: 2.0.0

---

## Authentication

Currently, the API is open for development. Production deployments should implement API key authentication.

---

## Endpoints

### 1. Scan Single Text

**POST** `/api/scan`

Scan a single text for Fair Housing Act violations.

#### Request Body

```json
{
  "text": "Luxury apartment perfect for young professionals",
  "jurisdictions": ["california", "nyc"],
  "use_cache": true
}
```

#### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | Yes | The listing text to scan |
| `jurisdictions` | array | No | List of jurisdictions (default: federal only) |
| `use_cache` | boolean | No | Enable caching (default: true) |

#### Response

```json
{
  "score": 75,
  "is_safe": true,
  "flagged_items": []
}
```

#### Example

```bash
curl -X POST http://localhost:8000/api/scan \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Beautiful home near churches",
    "jurisdictions": ["california"]
  }'
```

---

### 2. Batch Scan

**POST** `/api/scan/batch`

Scan multiple texts in a single request for improved efficiency.

#### Request Body

```json
{
  "items": [
    {
      "text": "First listing text",
      "jurisdictions": ["california"],
      "use_cache": true
    },
    {
      "text": "Second listing text",
      "jurisdictions": ["nyc", "uk"],
      "use_cache": true
    }
  ]
}
```

#### Response

```json
{
  "results": [
    {
      "score": 100,
      "is_safe": true,
      "flagged_items": []
    },
    {
      "score": 50,
      "is_safe": false,
      "flagged_items": [...]
    }
  ],
  "total_scanned": 2,
  "total_violations": 1
}
```

#### Example

```bash
curl -X POST http://localhost:8000/api/scan/batch \
  -H "Content-Type: application/json" \
  -d @batch_request.json
```

---

### 3. Reload Rules

**POST** `/api/reload-rules`

Hot-reload rules from disk without restarting the service.

#### Response

```json
{
  "status": "success",
  "message": "Rules reloaded: 251 → 300",
  "old_count": 251,
  "new_count": 300
}
```

#### Example

```bash
curl -X POST http://localhost:8000/api/reload-rules
```

---

### 4. Health Check

**GET** `/api/health`

Check API health and system status.

#### Response

```json
{
  "status": "healthy",
  "service": "FairProp API",
  "version": "2.0.0",
  "ai_available": true,
  "rules_loaded": 300,
  "jurisdictions_supported": "100+"
}
```

---

### 5. Usage Statistics

**GET** `/api/stats`

Get API usage statistics.

#### Response

```json
{
  "total_scans": 1523,
  "total_violations": 342,
  "violation_rate": "22.5%"
}
```

---

## Python Client Example

```python
import requests

# Single scan
response = requests.post('http://localhost:8000/api/scan', json={
    'text': 'Perfect for a young bachelor',
    'jurisdictions': ['california', 'nyc']
})

result = response.json()
print(f"Score: {result['score']}/100")
print(f"Safe: {result['is_safe']}")

# Batch scan
batch_response = requests.post('http://localhost:8000/api/scan/batch', json={
    'items': [
        {'text': 'First listing'},
        {'text': 'Second listing'}
    ]
})

batch_result = batch_response.json()
print(f"Total scanned: {batch_result['total_scanned']}")
print(f"Violations: {batch_result['total_violations']}")
```

---

## JavaScript Client Example

```javascript
// Single scan
const response = await fetch('http://localhost:8000/api/scan', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: 'Luxury apartment near synagogue',
    jurisdictions: ['california']
  })
});

const result = await response.json();
console.log(`Score: ${result.score}/100`);
console.log(`Safe: ${result.is_safe}`);
```

---

## Supported Jurisdictions

### United States (51)
All 50 states + DC. Use lowercase state names: `california`, `texas`, `new_york`, `dc`

### International (40+)
- **Canada**: `canada`
- **Europe**: `uk`, `germany`, `france`, `spain`, `italy`, etc.
- **Asia**: `china`, `japan`, `south_korea`, `singapore`, etc.
- **Latin America**: `brazil`, `mexico`, `argentina`, etc.
- **Middle East**: `uae`, `saudi_arabia`, `israel`, `turkey`
- **Africa**: `south_africa`, `nigeria`, `kenya`, etc.
- **Oceania**: `australia`, `new_zealand`

See [GLOBAL_REFERENCE.md](GLOBAL_REFERENCE.md) for complete list.

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (invalid parameters) |
| 500 | Internal Server Error |

---

## Rate Limiting

Currently no rate limiting in development. Production deployments should implement rate limiting based on API keys.

---

## Performance

- **Caching**: Enabled by default, stores up to 1000 recent scans
- **Batch Processing**: Up to 100 items per batch recommended
- **Response Time**: < 200ms for cached requests, < 1s for uncached

---

## Interactive Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

Visit `http://localhost:8000/redoc` for ReDoc documentation.
