# Rules Engine Architecture

FairProp's core value proposition is its **deterministic explainability** combined with **probabilistic AI safety nets**. This document explains how the rules engine processes text.

## 🏗️ The 3-Layer "Swiss Cheese" Model
We use a layered approach to balance performance (latency) with accuracy (recall).

### Layer 1: Deterministic Rules (Regex & Fuzzy)
*~1ms latency*
- **Mechanism**: Aho-Corasick string matching and optimized RegEx patterns.
- **Purpose**: Catch "Low Hanging Fruit" (e.g., "No kids", "White only").
- **Config**: Defined in JSON (e.g., `rules/federal/fha.json`).
- **Explainability**: 100%. We can point to the exact word and the specific law section.

### Layer 2: Semantic Vector Search (Contextual)
*~15ms latency*
- **Mechanism**: `SentenceTransformers` (all-MiniLM-L6-v2) embedding input text + ChromaDB query.
- **Purpose**: Catch paraphrases that avoid keywords.
    - *Example*: "Perfect for active lifestyles" (Implies ableism/ageism).
- **Thresholding**: Cosine similarity > 0.75 (tunable).

### Layer 3: Neural Guardrail (Intent Classifier)
*~100ms latency*
- **Mechanism**: Zero-shot classification (BART-large-mnli) or fine-tuned BERT.
- **Purpose**: Disambiguation.
    - *Example*: "Walking distance to Catholic church" (Location description vs. Religious steering).
- **Logic**: If Layer 1 & 2 are unsure (score 0.4-0.6), Layer 3 assists.

## 🔄 Rule Loading & Precedence
1. **Global Rules**: Loaded first (Base FHA).
2. **Jurisdiction Overrides**: Loaded second. Specific state rules can *add* to or *modify* sensitivity.
   - *Example*: "Source of Income" is NOT protected federally but IS protected in CA/NY.
   - If `jurisdictions=['US-CA']`, the engine enables `source_of_income` checks.

## 🛠️ Data Structure
Rules are stored as standardized JSON objects:

```json
{
  "id": "FHA-FAM-001",
  "category": "Familial Status",
  "severity": "High",
  "patterns": [
    "no children",
    "adults only",
    "singles only"
  ],
  "associated_laws": ["Fair Housing Act Sec. 804(c)"],
  "suggestion": "Describe the property, not the tenant."
}
```

This structure ensures that every flag is traceable to a specific rule definition, essential for audit trails.
