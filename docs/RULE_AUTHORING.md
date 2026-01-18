# Rule Authoring Guide

## 📝 Overview

This guide explains how to create custom fair housing rules for FairProp.

---

## Rule Structure

### Basic Rule Format

```json
{
  "id": "JURISDICTION-CATEGORY-NUMBER",
  "category": "Human-readable category",
  "trigger_words": ["phrase 1", "phrase 2", "phrase 3"],
  "severity": "Critical|Warning|Info",
  "legal_basis": "Legal citation or reference",
  "suggestion": "How to fix the violation"
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier (e.g., `FHA-RACE-001`) |
| `category` | string | Yes | Violation category (e.g., "Race", "Religion") |
| `trigger_words` | array | Yes | List of phrases that trigger this rule |
| `severity` | string | Yes | `Critical`, `Warning`, or `Info` |
| `legal_basis` | string | Yes | Legal citation or standard |
| `suggestion` | string | Yes | Guidance on how to fix |

---

## ID Naming Convention

### Format
```
{JURISDICTION}-{CATEGORY}-{NUMBER}
```

### Examples
- `FHA-RACE-001` - Federal Fair Housing Act, Race category, rule #1
- `CA-SOI-001` - California, Source of Income, rule #1
- `NYC-CRIM-001` - New York City, Criminal History, rule #1
- `UK-AGE-001` - United Kingdom, Age, rule #1

### Jurisdiction Codes
- **Federal US**: `FHA`
- **US States**: Two-letter code (e.g., `CA`, `NY`, `TX`)
- **US Cities**: City abbreviation (e.g., `NYC`, `LA`, `SF`)
- **Countries**: ISO 3166-1 alpha-2 (e.g., `UK`, `CA`, `AU`, `DE`)

### Category Codes (Suggested)
- `RACE` - Race/Ethnicity
- `REL` - Religion
- `SEX` - Sex/Gender
- `FAM` - Familial Status
- `HAND` - Handicap/Disability
- `NAT` - National Origin
- `SOI` - Source of Income
- `LGBTQ` - Sexual Orientation/Gender Identity
- `AGE` - Age
- `CRIM` - Criminal History
- `MIL` - Military/Veteran Status

---

## Trigger Words Best Practices

### 1. Be Specific
```json
// ❌ Too broad
"trigger_words": ["family"]

// ✅ Specific context
"trigger_words": ["no families", "adults only", "no children allowed"]
```

### 2. Include Variations
```json
"trigger_words": [
  "no section 8",
  "no vouchers",
  "no housing assistance",
  "no government assistance",
  "employment income only"
]
```

### 3. Consider Typos
The fuzzy matcher will catch minor typos, but include common misspellings:
```json
"trigger_words": [
  "handicapped",
  "handicap",
  "disabled",
  "disability"
]
```

### 4. Multi-word Phrases
Use complete phrases for context:
```json
// ✅ Good
"trigger_words": ["perfect for young professionals"]

// ❌ Too generic
"trigger_words": ["young", "professionals"]
```

---

## Severity Levels

### Critical
**Use when**: Direct violation of law, high legal risk

**Examples**:
- "No blacks allowed"
- "Christians only"
- "No disabled"

**Penalty**: -25 points from compliance score

### Warning
**Use when**: Potentially problematic, needs review

**Examples**:
- "Perfect for young professionals" (age implication)
- "Near churches" (religion implication)
- "Family-friendly" (familial status)

**Penalty**: -10 points from compliance score

### Info
**Use when**: Best practice suggestion, not violation

**Examples**:
- "Consider adding Equal Housing Opportunity statement"
- "Describe property features, not ideal tenant"

**Penalty**: -5 points from compliance score

---

## Legal Basis

### Format
```
{Law Name}, {Citation} - {Specific Provision}
```

### Examples

**US Federal**:
```json
"legal_basis": "Fair Housing Act, 42 U.S.C. § 3604(a) - Prohibition of race discrimination"
```

**State**:
```json
"legal_basis": "California Fair Employment and Housing Act (FEHA), Gov. Code § 12955 - Source of Income Protection"
```

**International**:
```json
"legal_basis": "UK Equality Act 2010, Section 4 - Protected Characteristics (Age)"
```

**Universal**:
```json
"legal_basis": "Universal Declaration of Human Rights, Article 2 - Non-discrimination"
```

---

## Suggestion Writing

### Guidelines

1. **Be Specific**: Tell them exactly what to change
2. **Be Positive**: Suggest what to do, not just what not to do
3. **Provide Examples**: Show compliant alternatives

### Template
```
{Action} {Problematic Element}. {Alternative Approach}.
```

### Examples

**❌ Vague**:
```json
"suggestion": "Remove discriminatory language"
```

**✅ Specific**:
```json
"suggestion": "Remove age-related language like 'young professionals'. Instead, describe property features: 'Modern apartment with high-speed internet and co-working space.'"
```

**✅ With Example**:
```json
"suggestion": "Replace 'perfect for families' with neutral description: 'Spacious 3-bedroom home with large backyard and nearby parks.'"
```

---

## Complete Examples

### Example 1: Federal Rule
```json
{
  "id": "FHA-RACE-001",
  "category": "Race",
  "trigger_words": [
    "whites only",
    "caucasian preferred",
    "no blacks",
    "no african americans"
  ],
  "severity": "Critical",
  "legal_basis": "Fair Housing Act, 42 U.S.C. § 3604(a) - Prohibition of race discrimination in housing",
  "suggestion": "Remove all race-based language. Describe property features and amenities instead of preferred tenant characteristics."
}
```

### Example 2: State Rule
```json
{
  "id": "CA-SOI-001",
  "category": "Source of Income (California)",
  "trigger_words": [
    "no section 8",
    "no vouchers",
    "no housing assistance",
    "employment income only"
  ],
  "severity": "Critical",
  "legal_basis": "California Fair Employment and Housing Act (FEHA), Gov. Code § 12955(a) - Source of Income Protection",
  "suggestion": "California law prohibits discrimination based on source of income. Remove restrictions on housing vouchers and public assistance. State: 'All lawful sources of income accepted.'"
}
```

### Example 3: International Rule
```json
{
  "id": "UK-AGE-001",
  "category": "Age (United Kingdom)",
  "trigger_words": [
    "young professionals only",
    "retirees preferred",
    "over 50s",
    "under 30"
  ],
  "severity": "Critical",
  "legal_basis": "Equality Act 2010, Section 4 - Protected Characteristics (Age)",
  "suggestion": "Remove age-specific language. Focus on property features: 'Modern apartment convenient for commuters' instead of 'perfect for young professionals.'"
}
```

---

## Testing Your Rules

### 1. Create Test File
```json
// rules/test/my_new_rules.json
[
  {
    "id": "TEST-001",
    "category": "Test Category",
    "trigger_words": ["test phrase"],
    "severity": "Warning",
    "legal_basis": "Test Law",
    "suggestion": "Test suggestion"
  }
]
```

### 2. Test with CLI
```bash
# Scan with custom rules
fairprop scan test_listing.txt --rules rules/test/my_new_rules.json
```

### 3. Validate JSON
```bash
# Use jq to validate
cat rules/test/my_new_rules.json | jq .

# Or Python
python -m json.tool rules/test/my_new_rules.json
```

---

## Adding Rules to FairProp

### For New Jurisdictions

1. **Create file**: `rules/international/{country}.json` or `rules/us_states/{state}.json`

2. **Add to jurisdiction map** in `fairprop/auditor.py`:
```python
jurisdiction_map = {
    # ... existing entries
    'new_jurisdiction': 'rules/path/to/new_rules.json',
}
```

3. **Test**:
```bash
fairprop scan listing.txt -j new_jurisdiction
```

### For Existing Jurisdictions

1. **Edit file**: `rules/{jurisdiction}.json`

2. **Add new rule** to array

3. **Reload rules** (if API is running):
```bash
curl -X POST http://localhost:8000/api/reload-rules
```

---

## Common Patterns

### Pattern 1: Protected Class
```json
{
  "id": "{JURISDICTION}-{CLASS}-001",
  "category": "{Protected Class}",
  "trigger_words": ["no {class}", "{class} not allowed", "prefer non-{class}"],
  "severity": "Critical",
  "legal_basis": "{Law} - {Class} Protection",
  "suggestion": "Cannot discriminate based on {class}. Remove all {class}-related language."
}
```

### Pattern 2: Implicit Bias
```json
{
  "id": "{JURISDICTION}-IMPL-001",
  "category": "Implicit {Bias Type}",
  "trigger_words": ["perfect for {group}", "ideal for {group}"],
  "severity": "Warning",
  "legal_basis": "{Law} - Steering Prevention",
  "suggestion": "Avoid language that steers specific groups. Describe property features instead."
}
```

### Pattern 3: Visual Requirements
```json
{
  "id": "{JURISDICTION}-VIS-001",
  "category": "Visual Compliance",
  "trigger_words": ["(visual check)"],
  "severity": "Info",
  "legal_basis": "{Law} - Equal Housing Opportunity Logo Requirement",
  "suggestion": "Include Equal Housing Opportunity logo in all advertising materials."
}
```

---

## Multi-Language Rules

For international jurisdictions, include both local language and English:

```json
{
  "id": "DE-AGG-001",
  "category": "Ethnic Origin (Germany)",
  "trigger_words": [
    "nur deutsche",
    "keine ausländer",
    "german only",
    "no foreigners"
  ],
  "severity": "Critical",
  "legal_basis": "AGG § 19 - Allgemeines Gleichbehandlungsgesetz",
  "suggestion": "Darf nicht aufgrund ethnischer Herkunft diskriminieren. / Cannot discriminate based on ethnic origin."
}
```

---

## Rule Maintenance

### Regular Review
- Review rules quarterly
- Update based on new case law
- Add new trigger phrases from violations

### Version Control
```bash
# Track changes
git add rules/
git commit -m "Add new California source of income rules"
git push
```

### Documentation
- Document rationale for each rule
- Link to relevant case law
- Note jurisdiction-specific nuances

---

## Resources

- [Fair Housing Act](https://www.justice.gov/crt/fair-housing-act-1)
- [HUD Fair Housing Regulations](https://www.hud.gov/program_offices/fair_housing_equal_opp/fair_housing_act_overview)
- [State Fair Housing Laws](https://www.nfha.org/state-and-local-laws/)
- [International Human Rights Standards](https://www.ohchr.org/en/instruments-listings)

---

## Getting Help

- **GitHub Issues**: Report bugs or request features
- **Discussions**: Ask questions about rule authoring
- **Pull Requests**: Contribute new rules

---

**Remember**: Rules should be legally accurate, culturally sensitive, and practically useful. When in doubt, consult with a fair housing attorney.
