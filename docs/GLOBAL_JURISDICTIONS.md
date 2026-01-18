# FairProp Global Jurisdiction Guide

## Supported Regions

### 🇺🇸 United States
**Federal**: Fair Housing Act (FHA) - All 50 states
**State/Local**:
- California (FEHA) - Source of income, marital status, sexual orientation
- New York City (HRL) - Criminal history, immigration status, source of income
- Massachusetts, New Jersey, Washington, Oregon, Colorado, Connecticut, Minnesota, Illinois - Common state protections

### 🇨🇦 Canada
**Provinces**:
- Ontario - Receipt of public assistance, family status
- British Columbia - Lawful source of income
- Quebec - Civil status protections
**Federal**: Canadian Human Rights Act - Indigenous status protection

### 🇦🇺 Australia
**Federal**:
- Racial Discrimination Act 1975
- Disability Discrimination Act 1992
**States**:
- New South Wales - Transgender status
- Victoria - Personal association
- Queensland - Lawful sexual activity

### 🇬🇧 United Kingdom
**England, Wales, Scotland**: Equality Act 2010
- Age, religion, pregnancy/maternity, marriage/civil partnership, gender reassignment

### 🌏 Asia-Pacific
- **Singapore**: Race, religion, language (Ethnic Integration Policy)
- **Hong Kong**: Race, disability discrimination ordinances
- **Japan**: Nationality, gender equality

## Usage Examples

### Single Jurisdiction
```bash
fairprop scan listing.txt -j canada
```

### Multiple Jurisdictions
```bash
fairprop scan listing.txt -j california -j canada -j uk
```

### Python API
```python
from fairprop import FairHousingAuditor

# Global compliance check
auditor = FairHousingAuditor(jurisdictions=['california', 'canada', 'uk', 'australia'])
report = auditor.scan_text(text)
```

## Adding New Jurisdictions

To add a new jurisdiction:
1. Create a JSON file in `rules/international/` or `rules/us_states/`
2. Follow the rule schema (see existing files)
3. Add mapping in `fairprop/auditor.py` jurisdiction_map
4. Update this guide

## Legal Disclaimer

FairProp provides automated compliance checks based on publicly available fair housing laws. This tool:
- ✅ Helps identify potential violations
- ✅ Provides educational guidance
- ❌ Is NOT legal advice
- ❌ Does not replace consultation with local legal experts

Always consult with a qualified attorney familiar with local housing laws.
