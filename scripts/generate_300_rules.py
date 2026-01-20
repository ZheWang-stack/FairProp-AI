"""
Comprehensive Rule Generation Script for 300+ Rules
Generates industry-leading fair housing compliance rules
"""
import json
from pathlib import Path

# Strategy:
# 1. Federal Rules: 45 → 120 (add 75 more)
# 2. State Rules: 15 states × 8 rules = 120
# 3. City Rules: 20 cities × 3 rules = 60
# Total: 120 + 120 + 60 = 300

print("Generating 300+ comprehensive fair housing rules...")
print("=" * 60)

# Load existing 45 rules
with open('fha_rules.json', 'r', encoding='utf-8') as f:
    existing_rules = json.load(f)

print(f"Existing rules: {len(existing_rules)}")

# We'll generate additional federal rules to reach 120 total
# This means adding 75 more federal rules

additional_federal_rules = []

# Race/Color - expand to 15 total (currently ~6)
race_rules_expansion = [
    {
        "id": "FHA-RACE-006",
        "category": "Race",
        "trigger_words": ["diverse", "multicultural", "mixed neighborhood", "integrated", "rainbow community", "all backgrounds"],
        "severity": "Warning",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "Avoid describing racial composition. Focus on property features and location."
    },
    {
        "id": "FHA-RACE-007",
        "category": "Race",
        "trigger_words": ["ethnic", "cultural diversity", "minority-majority", "predominantly", "homogeneous"],
        "severity": "Warning",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "Describe neighborhood amenities without racial or ethnic references."
    },
    {
        "id": "FHA-RACE-008",
        "category": "Race",
        "trigger_words": ["white flight", "changing neighborhood", "transitioning area", "gentrifying"],
        "severity": "Critical",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "Describe development and improvements without racial implications."
    },
    {
        "id": "FHA-RACE-009",
        "category": "Race",
        "trigger_words": ["country club", "private club", "members only", "exclusive membership"],
        "severity": "Warning",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "Describe amenities without exclusionary language."
    }
]

additional_federal_rules.extend(race_rules_expansion)

# Religion - expand to 10 total (currently ~4)
religion_rules_expansion = [
    {
        "id": "FHA-RELG-005",
        "category": "Religion",
        "trigger_words": ["faith-based", "religious community", "believers", "god-fearing", "spiritual"],
        "severity": "Warning",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "Avoid religious characterizations of residents or community."
    },
    {
        "id": "FHA-RELG-006",
        "category": "Religion",
        "trigger_words": ["bible study", "prayer group", "worship service", "religious gathering"],
        "severity": "Warning",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "Describe community activities without religious specificity."
    }
]

additional_federal_rules.extend(religion_rules_expansion)

# Sex/Gender - expand to 12 total (currently ~5)
sex_rules_expansion = [
    {
        "id": "FHA-SEX-006",
        "category": "Sex",
        "trigger_words": ["ladies", "gentlemen", "boys", "girls", "guys", "gals"],
        "severity": "Warning",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "Use gender-neutral terms like 'residents', 'tenants', or 'occupants'."
    },
    {
        "id": "FHA-SEX-007",
        "category": "Sex",
        "trigger_words": ["female roommate", "male tenant", "women's housing", "men's residence"],
        "severity": "Critical",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "Remove gender restrictions. Housing must be open to all genders."
    }
]

additional_federal_rules.extend(sex_rules_expansion)

# Disability - expand to 15 total (currently ~6)
disability_rules_expansion = [
    {
        "id": "FHA-HAND-007",
        "category": "Handicap",
        "trigger_words": ["physically fit", "able to climb", "mobility required", "must be mobile"],
        "severity": "Critical",
        "legal_basis": "42 U.S.C. § 3604(f)",
        "suggestion": "Describe property features (e.g., 'third floor') without ability requirements."
    },
    {
        "id": "FHA-HAND-008",
        "category": "Handicap",
        "trigger_words": ["hearing required", "must be able to hear", "visual acuity", "sight required"],
        "severity": "Critical",
        "legal_basis": "42 U.S.C. § 3604(f)",
        "suggestion": "Do not impose sensory ability requirements."
    },
    {
        "id": "FHA-HAND-009",
        "category": "Handicap",
        "trigger_words": ["mental health", "psychiatric", "cognitive ability", "sound mind"],
        "severity": "Critical",
        "legal_basis": "42 U.S.C. § 3604(f)",
        "suggestion": "Do not discriminate based on mental health or cognitive disabilities."
    }
]

additional_federal_rules.extend(disability_rules_expansion)

# Familial Status - expand to 15 total (currently ~6)
familial_rules_expansion = [
    {
        "id": "FHA-FAM-007",
        "category": "Familial Status",
        "trigger_words": ["pregnant", "expecting", "maternity", "newborn", "infant"],
        "severity": "Critical",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "Do not reference pregnancy or children in housing descriptions."
    },
    {
        "id": "FHA-FAM-008",
        "category": "Familial Status",
        "trigger_words": ["childless", "no dependents", "independent living", "solo lifestyle"],
        "severity": "Warning",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "Avoid implying preference for households without children."
    },
    {
        "id": "FHA-FAM-009",
        "category": "Familial Status",
        "trigger_words": ["family size", "number of children", "kids allowed", "child limit"],
        "severity": "Critical",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "Do not limit or specify family size or number of children."
    }
]

additional_federal_rules.extend(familial_rules_expansion)

# National Origin - expand to 12 total (currently ~5)
national_origin_rules_expansion = [
    {
        "id": "FHA-NAT-006",
        "category": "National Origin",
        "trigger_words": ["passport required", "citizenship", "green card", "visa status", "documentation"],
        "severity": "Critical",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "Request only standard identification required of all applicants."
    },
    {
        "id": "FHA-NAT-007",
        "category": "National Origin",
        "trigger_words": ["cultural fit", "american culture", "western values", "local customs"],
        "severity": "Warning",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "Avoid cultural or national origin preferences."
    }
]

additional_federal_rules.extend(national_origin_rules_expansion)

# Age - expand to 12 total (currently ~5)
age_rules_expansion = [
    {
        "id": "FHA-AGE-006",
        "category": "Age",
        "trigger_words": ["age limit", "minimum age", "maximum age", "age requirement", "age restriction"],
        "severity": "Critical",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "Remove age restrictions unless qualified HOPA community."
    },
    {
        "id": "FHA-AGE-007",
        "category": "Age",
        "trigger_words": ["older adults", "middle-aged", "prime of life", "seasoned", "experienced"],
        "severity": "Warning",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "Avoid age-related descriptors for ideal tenants."
    }
]

additional_federal_rules.extend(age_rules_expansion)

# Economic Status - expand to 10 total (currently ~3)
economic_rules_expansion = [
    {
        "id": "FHA-ECON-004",
        "category": "Economic Status",
        "trigger_words": ["income requirement", "minimum salary", "credit score", "financial status"],
        "severity": "Warning",
        "legal_basis": "State/Local Laws (varies)",
        "suggestion": "Apply income/credit requirements uniformly to all applicants."
    },
    {
        "id": "FHA-ECON-005",
        "category": "Economic Status",
        "trigger_words": ["working class", "blue collar", "labor", "service workers"],
        "severity": "Warning",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "Avoid economic class characterizations."
    }
]

additional_federal_rules.extend(economic_rules_expansion)

# Implicit Bias - expand to 15 total (currently ~5)
implicit_bias_rules_expansion = [
    {
        "id": "FHA-IMPL-006",
        "category": "Implicit Bias",
        "trigger_words": ["sketchy", "rough", "bad area", "dangerous", "crime-ridden"],
        "severity": "Warning",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "Provide objective crime statistics if relevant, avoid subjective characterizations."
    },
    {
        "id": "FHA-IMPL-007",
        "category": "Implicit Bias",
        "trigger_words": ["nice people", "good neighbors", "quality residents", "respectable"],
        "severity": "Warning",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "Avoid subjective characterizations of residents."
    },
    {
        "id": "FHA-IMPL-008",
        "category": "Implicit Bias",
        "trigger_words": ["established", "settled", "stable", "rooted", "long-term residents"],
        "severity": "Warning",
        "legal_basis": "42 U.S.C. § 3604(c)",
        "suggestion": "Describe community without implying preference for certain resident types."
    }
]

additional_federal_rules.extend(implicit_bias_rules_expansion)

print(f"Generated {len(additional_federal_rules)} additional federal rules")
print(f"Total federal rules will be: {len(existing_rules) + len(additional_federal_rules)}")

# Save preview
preview = {
    "current_count": len(existing_rules),
    "additional_federal": len(additional_federal_rules),
    "projected_federal_total": len(existing_rules) + len(additional_federal_rules),
    "sample_new_rules": additional_federal_rules[:5]
}

with open('rule_generation_preview.json', 'w', encoding='utf-8') as f:
    json.dump(preview, f, indent=2, ensure_ascii=False)

print("\nPreview saved to rule_generation_preview.json")
print("Next: Generate state and city rules to reach 300 total")
