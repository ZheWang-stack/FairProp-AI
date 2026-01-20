# Jurisdiction Coverage (v2.0)

> **Scope Definition**: FairProp AI provides structured rule sets for screening potential advertising violations. "Coverage" indicates that specific logic (regex, keywords, or semantic vectors) has been implemented for a region's protected classes. **It does not imply a guarantee of complete legal compliance.**

## 🌎 Summary
- **Primary Framework**: United States (Federal FHA)
- **Extended Frameworks**: state-level overrides, International (GDPR/Equality Act principles)

## 🇺🇸 United States
### Federal
- **Law**: Fair Housing Act (Title VIII of the Civil Rights Act of 1968)
- **Protected Classes**: Race, Color, Religion, National Origin, Sex, Disability, Familial Status.
- **Status**: ✅ Full Rule Support

### State-Level Specifics (Examples)
FairProp extends federal rules with state-specific protected classes (e.g., "Source of Income", "Gender Identity").

| State | Additional Protected Classes | Rule ID Prefix |
|:---|:---|:---|
| **California** | Source of Income, Marital Status, Sexual Orientation, Gender Identity, Genetic Info | `US-CA-*` |
| **New York** | Age, Marital Status, Military Status, Sexual Orientation | `US-NY-*` |
| **Massachusetts** | Source of Income (Section 8), Miltary Status | `US-MA-*` |
| ... | *Generic support for remaining 47 states* | `US-*` |

## 🇪🇺 European Union
### Principles
Based on the **EU Racial Equality Directive (2000/43/EC)** and general non-discrimination principles.
- **Focus**: Direct discrimination in access to goods and services (housing).
- **Status**: ⚠️ Beta (General Principles Only)

## 🇬🇧 United Kingdom
- **Law**: Equality Act 2010
- **Supported Checks**: "No DSS" (Source of Income equivalent), Race, Disability, Religion.
- **Status**: ⚠️ Beta

## 🇨🇦 Canada
- **Law**: Canadian Human Rights Act
- **Provincial Codes**: Examples included for Ontario (Human Rights Code) and BC.
- **Status**: ⚠️ Beta

---

### 🔧 Extensibility
FairProp is designed to be **jurisdiction-agnostic**. The `RuleEngine` loads JSON schemas dynamically.

**Adding a new jurisdiction:**
1. Create `rules/international/{country_code}.json`
2. Define protected categories and regex patterns.
3. Reload engine.

See [Rule Authoring Guide](RULE_AUTHORING.md) for details.
