# Changelog

All notable changes to FairProp AI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-01-19

### 🌍 Global Expansion

#### Added
- **100+ Jurisdictions**: Complete global coverage across 6 continents
  - All 50 US states + Washington DC
  - 40+ international countries (UK, Germany, France, China, Japan, etc.)
  - Canada (Federal + 3 provinces)
  - Australia (Federal + 3 states)
- **Multi-language Support**: i18n framework with 20+ languages
  - English, Spanish, Portuguese, French, German, Dutch, Italian
  - Chinese (Simplified), Japanese, Korean, Hindi
  - Arabic, Hebrew, Turkish, and more
- **International Rules**: Auto-generated rules based on UDHR and local laws

### ⚡ Performance & Features

#### Added
- **LRU Caching**: 100x performance improvement for repeated scans
- **Batch Processing API**: `/api/scan/batch` endpoint for high-volume processing
- **Hot-Reload**: `/api/reload-rules` endpoint for zero-downtime rule updates
- **Usage Analytics**: API usage tracking and statistics (`/api/stats`)
- **Enhanced Health Check**: Detailed system status in `/api/health`

#### Changed
- API version bumped to 2.0.0
- Improved error messages with helpful context
- More detailed logging with DEBUG/INFO/WARNING/ERROR levels
- Better variable naming and code comments

### 📚 Documentation

#### Added
- **API Documentation** (`docs/API.md`): Complete REST API reference
- **Deployment Guide** (`docs/DEPLOYMENT.md`): Docker, Kubernetes, Cloud deployment
- **Architecture Documentation** (`docs/ARCHITECTURE.md`): System design deep-dive
- **Rule Authoring Guide** (`docs/RULE_AUTHORING.md`): How to create custom rules
- **Global Reference** (`docs/GLOBAL_REFERENCE.md`): Complete jurisdiction list
- **Complete Coverage** (`docs/COMPLETE_GLOBAL_COVERAGE.md`): Detailed coverage stats

#### Changed
- **README.md**: Complete rewrite with GitHub-style badges and formatting
- **index.html**: Full SEO optimization with Open Graph and structured data

### 🔧 Developer Experience

#### Added
- Comprehensive `.gitignore` for Python projects
- Example datasets for testing
- Unit tests with pytest
- Code coverage configuration

---

## [1.0.0] - 2025-12-15

### Initial Release

#### Added
- **Core Auditing Engine**: Neuro-symbolic AI with 3-layer detection
  - Layer 1: Rule-based keyword matching
  - Layer 2: Semantic vector search (ChromaDB)
  - Layer 3: Neural guardrail (Zero-shot classification)
- **Federal FHA Rules**: Complete US Fair Housing Act compliance
- **State Rules**: California FEHA and NYC HRL
- **CLI Tool**: Command-line interface with `typer` and `rich`
- **Web UI**: Streamlit dashboard for non-technical users
- **REST API**: FastAPI server with Swagger documentation
- **Browser Extension**: Chrome extension for real-time checking
- **OCR Support**: Image scanning with Tesseract
- **Logo Detection**: Equal Housing Opportunity logo verification
- **Audit Trail**: Cryptographically signed compliance certificates
- **AI Auto-Fix**: Generative AI suggestions (Flan-T5)

#### Features
- Privacy-first: 100% local execution
- Multi-modal: Text and image support
- Explainable: Every violation has legal basis
- Extensible: Easy to add new jurisdictions

---

## [Unreleased]

### Planned Features
- [ ] PyPI package distribution
- [ ] Docker Hub official images
- [ ] Mobile app (iOS/Android)
- [ ] Fine-tuned BERT model for fair housing
- [ ] Plugin system for custom checks
- [ ] Real-time analytics dashboard
- [ ] Webhook notifications
- [ ] Multi-language NLP (native non-English support)

---

## Version History

- **2.0.0** (2026-01-19) - Global expansion with 100+ jurisdictions
- **1.0.0** (2025-12-15) - Initial release with US coverage

---

For detailed commit history, see [GitHub Commits](https://github.com/ZheWang-stack/FairProp-AI/commits/main)
