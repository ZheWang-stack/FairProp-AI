# FairProp Global Jurisdiction Reference

## Complete Coverage: 70+ Jurisdictions

### 🇺🇸 United States (51)
**Federal + All 50 States + DC**

#### Usage
```bash
fairprop scan listing.txt -j california -j texas -j new_york -j florida
```

#### States with Additional Protections
- **Source of Income (18)**: CA, CO, CT, DE, DC, IL, ME, MD, MA, MN, NJ, NY, ND, OK, OR, UT, VT, WA
- **LGBTQ+ (24)**: CA, CO, CT, DE, DC, HI, IL, IA, ME, MD, MA, MN, NV, NH, NJ, NM, NY, OR, RI, UT, VT, VA, WA, WI
- **Marital Status (23)**: AK, CA, CO, CT, DE, DC, HI, IL, IA, ME, MD, MA, MI, MN, MT, NH, NJ, NY, ND, OR, VT, WA, WI

### 🇨🇦 Canada (4)
**Federal + 3 Provinces**

```bash
fairprop scan listing.txt -j canada
```

- Federal: Indigenous status protection
- Ontario: Public assistance, family status
- British Columbia: Lawful source of income
- Quebec: Civil status

### 🇲🇽 Mexico (1)
**Federal Anti-Discrimination Law**

```bash
fairprop scan listing.txt -j mexico --language es
```

- LFPED: Indigenous peoples, pregnancy, sexual orientation
- Bilingual: Spanish/English

---

### 🇬🇧 United Kingdom (1)
**Equality Act 2010**

```bash
fairprop scan listing.txt -j uk
```

- Age, religion, pregnancy, marriage, gender reassignment

### 🇩🇪 Germany (1)
**AGG (Allgemeines Gleichbehandlungsgesetz)**

```bash
fairprop scan listing.txt -j germany --language de
```

- Ethnic origin, religion, disability, age, sexual identity
- Bilingual: German/English

### 🇫🇷 France (1)
**Code de la construction et de l'habitation**

```bash
fairprop scan listing.txt -j france --language fr
```

- Origin, family situation, religion, disability, sexual orientation
- Bilingual: French/English

### 🇳🇱 Netherlands (1)
**AWGB (Algemene wet gelijke behandeling)**

```bash
fairprop scan listing.txt -j netherlands --language nl
```

- Race, religion, sexual orientation, disability, civil status
- Bilingual: Dutch/English

---

### 🇦🇺 Australia (4)
**Federal + 3 States**

```bash
fairprop scan listing.txt -j australia
```

- Federal: Racial & Disability Discrimination Acts
- NSW: Transgender status
- Victoria: Personal association
- Queensland: Lawful sexual activity

### 🇸🇬 Singapore (1)
**Ethnic Integration Policy**

```bash
fairprop scan listing.txt -j singapore
```

- Race, religion, language protection

### 🇭🇰 Hong Kong (1)
**Race & Disability Discrimination Ordinances**

```bash
fairprop scan listing.txt -j hong_kong
```

### 🇯🇵 Japan (1)
**Human Rights Protection Act**

```bash
fairprop scan listing.txt -j japan
```

- Nationality, gender equality

---

### 🇧🇷 Brazil (1)
**Lei de Locações + Federal Constitution**

```bash
fairprop scan listing.txt -j brazil --language pt
```

- Race, origin, religion, disability, sexual orientation
- Bilingual: Portuguese/English

---

## Multi-Jurisdiction Examples

### Global Real Estate Company
```bash
fairprop scan listing.txt \
  -j california \
  -j canada \
  -j uk \
  -j germany \
  -j australia \
  -j singapore
```

### European Market
```bash
fairprop scan listing.txt -j uk -j germany -j france -j netherlands
```

### Latin America
```bash
fairprop scan listing.txt -j mexico -j brazil --language es
```

### Asia-Pacific
```bash
fairprop scan listing.txt -j australia -j singapore -j hong_kong -j japan
```

---

## Language Support

### Available Languages
- `en` - English
- `es` - Español (Spanish)
- `pt` - Português (Portuguese)
- `fr` - Français (French)
- `de` - Deutsch (German)
- `nl` - Nederlands (Dutch)
- `zh` - 中文 (Chinese)
- `ja` - 日本語 (Japanese)
- `ko` - 한국어 (Korean)

### Usage
```bash
fairprop scan listing.txt -j germany --language de
fairprop scan listing.txt -j brazil --language pt
fairprop scan listing.txt -j singapore --language zh
```

---

## Python API

```python
from fairprop import FairHousingAuditor

# Global compliance with language support
auditor = FairHousingAuditor(
    jurisdictions=['california', 'canada', 'uk', 'germany', 'brazil'],
    language='en'
)

report = auditor.scan_text("Your listing text here")
```

---

## Total Coverage Summary

| Region | Jurisdictions | Languages |
|--------|---------------|-----------|
| North America | 53 (US 51 + CA 1 + MX 1) | EN, ES |
| Europe | 4 (UK, DE, FR, NL) | EN, DE, FR, NL |
| Asia-Pacific | 5 (AU 4 + SG, HK, JP) | EN, ZH, JA, KO |
| Latin America | 2 (BR, MX) | ES, PT |
| **TOTAL** | **70+** | **9** |
