# Complete US State Coverage

FairProp now supports **all 50 US states + Washington DC**.

## Coverage by Protection Type

### 🏛️ Federal (All States)
All 50 states are covered by the **Fair Housing Act (FHA)** which prohibits discrimination based on:
- Race
- Color
- National Origin
- Religion
- Sex
- Familial Status
- Disability

### 📋 States with Additional Protections

#### Source of Income (18 jurisdictions)
Cannot refuse Section 8 vouchers or other lawful income:
- California, Colorado, Connecticut, Delaware, DC, Illinois, Maine, Maryland, Massachusetts, Minnesota, New Jersey, New York, North Dakota, Oklahoma, Oregon, Utah, Vermont, Washington

#### Sexual Orientation & Gender Identity (24 jurisdictions)
LGBTQ+ protections:
- California, Colorado, Connecticut, Delaware, DC, Hawaii, Illinois, Iowa, Maine, Maryland, Massachusetts, Minnesota, Nevada, New Hampshire, New Jersey, New Mexico, New York, Oregon, Rhode Island, Utah, Vermont, Virginia, Washington, Wisconsin

#### Marital Status (23 jurisdictions)
Cannot discriminate against single parents, unmarried couples:
- Alaska, California, Colorado, Connecticut, Delaware, DC, Hawaii, Illinois, Iowa, Maine, Maryland, Massachusetts, Michigan, Minnesota, Montana, New Hampshire, New Jersey, New York, North Dakota, Oregon, Vermont, Washington, Wisconsin

#### Military/Veteran Status (12 states)
- Alaska, California, Colorado, Connecticut, Delaware, Iowa, Maine, Massachusetts, New Mexico, Ohio, Oregon, Virginia

#### Age (7 states)
Age discrimination protections beyond federal HOPA:
- Alaska, Massachusetts, Michigan, New York, Pennsylvania, Rhode Island, Wisconsin

## Usage Examples

### Single State
```bash
fairprop scan listing.txt -j texas
fairprop scan listing.txt -j california
```

### Multiple States
```bash
fairprop scan listing.txt -j california -j new_york -j texas -j florida
```

### State + Federal
```bash
# Automatically includes federal FHA
fairprop scan listing.txt -j massachusetts
```

### All Protections (Multi-State Property)
```bash
fairprop scan listing.txt -j california -j new_york -j dc -j massachusetts
```

## State Name Formats

Use lowercase with underscores:
- ✅ `new_york`, `new_jersey`, `north_carolina`
- ✅ `dc` or `washington_dc` for Washington DC
- ❌ `New York`, `NY` (not supported yet)

## Federal-Only States

The following states primarily follow federal FHA without significant additional protections:
Alabama, Arizona, Arkansas, Florida, Georgia, Idaho, Indiana, Kansas, Kentucky, Louisiana, Mississippi, Missouri, Nebraska, North Carolina, South Carolina, South Dakota, Tennessee, Texas, West Virginia, Wyoming

These states still benefit from the federal FHA rules and AI-powered semantic analysis.
