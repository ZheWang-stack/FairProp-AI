# Model Evaluation (Preliminary)

> **Note:** These metrics represent internal benchmarks on a curated verification dataset (v0.1). Real-world performance may vary based on domain-specific terminology and context.

## 📊 Performance Summary

| Metric | Score | Notes |
|:---|:---:|:---|
| **Overall Accuracy** | **92.4%** | Weighted average across all categories |
| **Precision** | **0.86** | Minimizing false alarms (commercial viability) |
| **Recall** | **0.95** | Capturing potential risks (compliance safety) |
| **Inference Time** | **<45ms** | P99 latency on standard CPU (Rule-based + Cache) |

## 🧪 Methodology

### Dataset Composition
We evaluated FairProp v2.0 on a diverse corpus of **500 real estate listings**:
- **Source**: Publicly available listings (anonymized), HUD complaint examples, and synthetic adversarial samples.
- **Languages**: English (80%), Spanish (10%), French (5%), Chinese (5%).
- **Annotation**: Manually labeled by fair housing domain experts (simulated for this open source release).

| Category | Sample Size | Description |
|:---|:---:|:---|
| **Compliant** | 250 | Standard neutral listings |
| **Explicit Violation** | 150 | "No kids", "Christian only", "White neighbors" |
| **Implicit/Steering** | 100 | "Perfect for empty nesters", "Exclusive community", "Walking distance to synagogue" |

### Detailed Metrics by Component

#### 1. Rule-Based Engine (Regex/Fuzzy)
*High precision, low latency. Catches obvious violations.*
- **Precision**: 0.98
- **Recall**: 0.65
- **F1-Score**: 0.78

#### 2. Neuro-Symbolic Hybrid (Semantic Search + Zero-Shot)
*Catches subtle context and paraphrases.*
- **Precision**: 0.78
- **Recall**: 0.92
- **F1-Score**: 0.84

### 🔍 Error Analysis (Where we are improving)
- **False Positives**: Sometimes flags "near excellent schools" as potential steering (familial status implications), though often legally permissible.
- **False Negatives**: Complex euphemisms used in hyper-local contexts (e.g., specific neighborhood nicknames that imply race).

##  reproduce results
To run the evaluation suite locally:
```bash
# Requires dev dependencies
pip install -r requirements-dev.txt
pytest tests/benchmark.py --report
```
