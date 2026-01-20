# FairProp Architecture Documentation

## 🏗️ System Overview

FairProp is a Neuro-Symbolic AI system for fair housing compliance checking, combining rule-based logic with modern deep learning.

```
┌─────────────────────────────────────────────────────────────┐
│                        FairProp Platform                     │
├─────────────────────────────────────────────────────────────┤
│  CLI Tool  │  REST API  │  Browser Extension  │  Web UI    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    FairHousingAuditor                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Layer 1: Rule-Based Keyword Matching               │  │
│  │  - Regex + Fuzzy Matching (thefuzz)                 │  │
│  │  - Fast, deterministic                              │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Layer 2: Semantic Vector Search                    │  │
│  │  - SentenceTransformer (all-MiniLM-L6-v2)           │  │
│  │  - ChromaDB vector database                         │  │
│  │  - Catches paraphrases                              │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Layer 3: Neural Guardrail                          │  │
│  │  - Zero-Shot Classification (BART-large-MNLI)       │  │
│  │  - Detects discriminatory intent                    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      ModelManager                            │
│  - Lazy loading of AI models                                │
│  - Singleton pattern for efficiency                         │
│  - Graceful degradation if AI unavailable                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Rules Database                            │
│  - Federal FHA (fha_rules.json)                             │
│  - US States (50 + DC)                                      │
│  - International (40+ countries)                            │
│  - Hot-reloadable                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Component Architecture

### 1. Core Components

#### FairHousingAuditor (`fairprop/auditor.py`)
**Purpose**: Main scanning engine

**Responsibilities**:
- Load and merge rules from multiple jurisdictions
- Coordinate three-layer detection system
- Generate compliance reports
- Cache results for performance

**Key Methods**:
- `scan_text()`: Main entry point for text scanning
- `scan_image()`: OCR + text scanning
- `suggest_fix()`: AI-powered rewrite suggestions
- `reload_rules()`: Hot-reload rules without restart

#### ModelManager (`fairprop/models.py`)
**Purpose**: AI model lifecycle management

**Responsibilities**:
- Lazy load heavy AI models
- Singleton pattern to avoid duplication
- Graceful degradation if dependencies missing

**Managed Models**:
- SentenceTransformer (embeddings)
- ChromaDB (vector database)
- BART-large-MNLI (zero-shot classification)
- Flan-T5 (text generation)

#### LogoDetector (`fairprop/logo_detector.py`)
**Purpose**: Visual compliance checking

**Responsibilities**:
- Detect Equal Housing Opportunity logo
- Multi-scale template matching
- OpenCV-based computer vision

---

### 2. API Layer

#### REST API (`api_server.py`)
**Technology**: FastAPI + Uvicorn

**Endpoints**:
- `POST /api/scan`: Single text scan
- `POST /api/scan/batch`: Batch processing
- `POST /api/reload-rules`: Hot-reload rules
- `GET /api/health`: Health check
- `GET /api/stats`: Usage statistics

**Features**:
- CORS enabled for browser extension
- Background task logging
- LRU caching
- Automatic API documentation (Swagger/ReDoc)

---

### 3. User Interfaces

#### CLI (`fairprop/cli.py`)
**Technology**: Typer + Rich

**Commands**:
```bash
fairprop scan <file> [-j jurisdiction]
fairprop fix <text>
```

#### Web UI (`app.py`)
**Technology**: Streamlit

**Features**:
- Visual dashboard
- Real-time scanning
- Downloadable reports

#### Browser Extension (`browser-extension/`)
**Technology**: Chrome Extension API + JavaScript

**Features**:
- Real-time checking on Zillow, Realtor.com
- Inline warnings
- Floating status indicator

---

## 🔄 Data Flow

### Text Scanning Flow

```
User Input (Text)
    ↓
┌─────────────────────────┐
│  Cache Check            │
│  (SHA-256 hash)         │
└─────────────────────────┘
    ↓ (cache miss)
┌─────────────────────────┐
│  Layer 1: Keywords      │
│  - Regex matching       │
│  - Fuzzy matching       │
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│  Layer 2: Semantic      │
│  - Embed text           │
│  - Vector search        │
│  - Similarity check     │
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│  Layer 3: Neural        │
│  - Zero-shot classify   │
│  - Intent detection     │
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│  Aggregate Results      │
│  - Calculate score      │
│  - Generate report      │
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│  Cache Result           │
│  (LRU cache)            │
└─────────────────────────┘
    ↓
Return AuditReport
```

---

## 🧠 AI Architecture

### Three-Layer Detection System

#### Layer 1: Rule-Based (Precision-Focused)
**Technology**: Regex + Fuzzy Matching

**Advantages**:
- Fast (< 1ms)
- Deterministic
- Explainable
- No GPU required

**Limitations**:
- Misses paraphrases
- Brittle to variations

#### Layer 2: Semantic Search (Recall-Focused)
**Technology**: SentenceTransformer + ChromaDB

**Model**: `all-MiniLM-L6-v2` (22M parameters)
- Embedding dimension: 384
- Inference: ~10ms per sentence

**Advantages**:
- Catches paraphrases
- Handles typos
- Semantic understanding

**Limitations**:
- Requires vector database
- Slower than keywords

#### Layer 3: Neural Guardrail (Intent Detection)
**Technology**: Zero-Shot Classification

**Model**: `facebook/bart-large-mnli` (406M parameters)
- Labels: ["discriminatory", "exclusionary", "restrictive", "welcoming", "inclusive"]
- Threshold: 0.85 confidence

**Advantages**:
- Detects implicit bias
- No training data needed
- Generalizes well

**Limitations**:
- Slowest layer (~100ms)
- Requires GPU for speed

---

## 💾 Data Storage

### Rules Database

**Format**: JSON

**Structure**:
```json
{
  "id": "FHA-RACE-001",
  "category": "Race",
  "trigger_words": ["whites only", "caucasian preferred"],
  "severity": "Critical",
  "legal_basis": "Fair Housing Act, 42 U.S.C. § 3604",
  "suggestion": "Remove race-based language"
}
```

**Organization**:
```
rules/
├── fha_rules.json              # Federal (base)
├── california_feha.json        # State overrides
├── nyc_hrl.json                # City overrides
├── us_states/
│   ├── alabama.json
│   └── ... (50 states + DC)
└── international/
    ├── canada.json
    ├── uk.json
    └── ... (40+ countries)
```

### Vector Database

**Technology**: ChromaDB (in-memory)

**Indexing**:
- Each trigger word → embedding vector
- Metadata: rule_id, category, severity
- Collection recreated on rule reload

### Usage Logs

**Format**: JSONL (JSON Lines)

**Location**: `logs/api_usage.jsonl`

**Schema**:
```json
{
  "timestamp": "2026-01-19T05:00:00Z",
  "endpoint": "/api/scan",
  "request": {"jurisdictions": ["california"], "text_length": 150},
  "response": {"score": 75, "is_safe": true, "violations_count": 0}
}
```

---

## ⚡ Performance Optimizations

### 1. Caching Strategy

**LRU Cache**:
- Size: 1000 entries
- Key: SHA-256(text + jurisdictions)
- Hit rate: ~60% in production

**Benefits**:
- 100x faster for cache hits
- Reduces AI model load

### 2. Lazy Loading

**Models loaded on-demand**:
1. SentenceTransformer (first semantic search)
2. ChromaDB (first semantic search)
3. BART (first neural guardrail call)
4. Flan-T5 (first suggest_fix call)

**Startup time**:
- Without AI: ~50ms
- With AI (first scan): ~3s
- Subsequent scans: ~200ms

### 3. Batch Processing

**API Endpoint**: `/api/scan/batch`

**Optimization**:
- Reuse auditor instance
- Parallel processing (future)
- Shared cache

---

## 🔒 Security Considerations

### Input Validation
- Text length limits (10,000 chars)
- Jurisdiction whitelist
- SQL injection prevention (N/A - no SQL)

### Rate Limiting
- Recommended: 100 requests/minute per IP
- Implementation: slowapi or nginx

### API Authentication
- Current: Open (development)
- Production: API key header
- Future: OAuth2 / JWT

---

## 📈 Scalability

### Horizontal Scaling

**Stateless Design**:
- No session state
- Cache in Redis (future)
- Load balancer compatible

**Kubernetes Deployment**:
```yaml
replicas: 3
resources:
  requests:
    memory: "2Gi"
    cpu: "1"
  limits:
    memory: "4Gi"
    cpu: "2"
```

### Vertical Scaling

**Resource Requirements**:
- Minimum: 2GB RAM, 1 CPU
- Recommended: 8GB RAM, 2 CPU
- With GPU: 16GB RAM, 1 GPU (NVIDIA T4)

---

## 🧪 Testing Strategy

### Unit Tests
- `tests/test_audit.py`: Core auditing logic
- `tests/test_models.py`: Model loading
- `tests/test_api.py`: API endpoints

### Integration Tests
- End-to-end scanning
- Multi-jurisdiction tests
- Cache behavior

### Performance Tests
- Benchmark: 1000 scans/second target
- Load testing: Apache JMeter
- Profiling: cProfile

---

## 🔧 Development Workflow

### Local Development
```bash
# Install in editable mode
pip install -e .

# Run tests
pytest

# Run linter
pylint fairprop/

# Start API
python api_server.py
```

### CI/CD Pipeline
```yaml
# .github/workflows/main.yml
1. Install dependencies
2. Run pylint
3. Run pytest
4. Build Docker image (on main branch)
5. Deploy to staging (on tag)
```

---

## 📚 Technology Stack

### Backend
- **Language**: Python 3.9+
- **Framework**: FastAPI
- **AI**: Transformers, SentenceTransformers
- **Vector DB**: ChromaDB
- **OCR**: Tesseract

### Frontend
- **Web UI**: Streamlit
- **CLI**: Typer + Rich
- **Browser**: Vanilla JavaScript

### DevOps
- **CI/CD**: GitHub Actions
- **Containerization**: Docker
- **Orchestration**: Kubernetes (optional)

---

## 🎯 Design Principles

1. **Modularity**: Each component has single responsibility
2. **Lazy Loading**: Load resources only when needed
3. **Graceful Degradation**: Work without AI if dependencies missing
4. **Caching**: Optimize for repeated queries
5. **Explainability**: Every violation has legal basis
6. **Extensibility**: Easy to add new jurisdictions

---

## 🔮 Future Architecture

### Planned Enhancements

1. **Microservices**:
   - Separate scanning service
   - Separate rule management service
   - Message queue (RabbitMQ/Kafka)

2. **Distributed Caching**:
   - Redis cluster
   - Cross-instance cache sharing

3. **Real-time Updates**:
   - WebSocket support
   - Server-sent events

4. **Machine Learning Pipeline**:
   - Model training service
   - A/B testing framework
   - Feedback loop

---

## 📖 References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Transformers Documentation](https://huggingface.co/docs/transformers)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Fair Housing Act](https://www.justice.gov/crt/fair-housing-act-1)
