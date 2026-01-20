"""
Rule Library Expansion Script
Generates comprehensive fair housing rules based on legal research and real-world cases.
"""
import json
from pathlib import Path

# Load existing rules
with open('fha_rules.json', 'r', encoding='utf-8') as f:
    existing_rules = json.load(f)

print(f"Existing rules: {len(existing_rules)}")

# Expansion strategy:
# 1. Age discrimination (3 → 15 rules)
# 2. Disability (5 → 20 rules)
# 3. Familial Status (6 → 18 rules)
# 4. Race/Color (8 → 25 rules)
# 5. Religion (4 → 12 rules)
# 6. Sex/Gender (5 → 15 rules)
# 7. National Origin (5 → 15 rules)
# 8. New: Economic discrimination (10 rules)
# 9. New: Implicit bias (15 rules)

# Age Discrimination - Expanded
age_rules = [
    {
        "id": "FHA-AGE-001",
        "category": "Age",
        "trigger_words": ["young professionals", "millennials", "gen z", "recent grads", "young adults", "20s-30s", "under 40", "youthful", "energetic crowd", "fresh graduates"],
        "severity": "Warning",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "Describe property features without age-specific language. Use 'professionals' or 'working individuals'."
    },
    {
        "id": "FHA-AGE-002",
        "category": "Age",
        "trigger_words": ["seniors only", "55+", "62+", "retirees", "golden years", "mature adults", "elderly", "senior living", "retirement community", "age-restricted"],
        "severity": "Critical",
        "legal_basis": "42 U.S.C. § 3607(b)",
        "suggestion": "If not a qualified HOPA community, remove age restrictions. If qualified, ensure proper documentation."
    },
    {
        "id": "FHA-AGE-003",
        "category": "Age",
        "trigger_words": ["no students", "no college kids", "professional tenants only", "established professionals", "career-focused", "post-college", "working adults"],
        "severity": "Warning",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "Student status can correlate with age. Use 'quiet environment' or 'professional setting' instead."
    },
    {
        "id": "FHA-AGE-004",
        "category": "Age",
        "trigger_words": ["active lifestyle", "dynamic environment", "fast-paced", "vibrant community", "energetic", "youthful atmosphere"],
        "severity": "Warning",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "These terms may imply age preference. Describe specific amenities instead."
    },
    {
        "id": "FHA-AGE-005",
        "category": "Age",
        "trigger_words": ["quiet for retirees", "peaceful retirement", "senior-friendly", "age-appropriate", "mature community", "settled neighborhood"],
        "severity": "Warning",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "Use 'quiet neighborhood' or 'peaceful setting' without age references."
    }
]

print(f"Generated {len(age_rules)} age discrimination rules")

# Save to file for review
output = {
    "expansion_summary": {
        "age_rules": len(age_rules),
        "total_new_trigger_words": sum(len(r["trigger_words"]) for r in age_rules)
    },
    "sample_rules": age_rules[:3]
}

with open('rule_expansion_preview.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("Preview saved to rule_expansion_preview.json")
