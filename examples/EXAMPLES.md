# Example Listings for Testing

## Clean Listings (Should Pass)

### Example 1: Professional Description
```
Beautiful 3-bedroom, 2-bathroom home in a quiet neighborhood. Features include:
- Modern kitchen with stainless steel appliances
- Spacious living room with hardwood floors
- Large backyard perfect for entertaining
- Attached 2-car garage
- Close to schools, shopping, and public transportation

Rent: $2,500/month
Contact: (555) 123-4567
```

### Example 2: Apartment Listing
```
Luxury 2-bedroom apartment in downtown high-rise building.

Amenities:
- 24/7 concierge service
- Fitness center and pool
- In-unit washer/dryer
- Floor-to-ceiling windows with city views
- Pet-friendly building

Available immediately. Schedule a viewing today!
```

---

## Problematic Listings (Should Fail)

### Example 3: Age Discrimination
```
Perfect starter home for young professionals! This modern condo is ideal for 
millennials looking to get on the property ladder. Not suitable for retirees.
```

**Violations:**
- "young professionals" - Age discrimination (implicit)
- "Not suitable for retirees" - Age discrimination (explicit)

---

### Example 4: Familial Status Discrimination
```
Adults-only building. No children allowed. Perfect for singles and couples 
without kids. Quiet environment guaranteed.
```

**Violations:**
- "Adults-only" - Familial status discrimination
- "No children allowed" - Familial status discrimination (explicit)

---

### Example 5: Religious Discrimination
```
Beautiful home near St. Mary's Church and Christian Community Center. 
Perfect for church-going families. Close to Sunday services.
```

**Violations:**
- Religious steering (implicit preference for Christians)

---

### Example 6: Source of Income (California)
```
Luxury apartment in San Francisco. Employment verification required.
No Section 8 vouchers. No housing assistance accepted.
```

**Violations (California only):**
- "No Section 8 vouchers" - Source of income discrimination
- "No housing assistance" - Source of income discrimination

---

### Example 7: Multiple Violations
```
Exclusive community for young Christian professionals. No children, no pets.
Must have stable employment - no government assistance. Perfect for 
traditional American families.
```

**Violations:**
- Age discrimination ("young")
- Religious discrimination ("Christian")
- Familial status ("No children")
- Source of income ("no government assistance")
- National origin (implicit - "traditional American")

---

## Edge Cases

### Example 8: Borderline Language
```
Family-friendly neighborhood with excellent schools nearby. Great for 
growing families. Spacious home with multiple bedrooms.
```

**Analysis:**
- "Family-friendly" - May trigger warning (steering)
- "Great for growing families" - Potential familial status steering
- Context matters: describing neighborhood vs. restricting tenants

---

### Example 9: Accessibility Features
```
Wheelchair accessible apartment on ground floor. Wide doorways, roll-in shower,
accessible kitchen. Perfect for individuals with mobility needs.
```

**Analysis:**
- Should PASS - Describing accessibility features is allowed
- Not discriminatory to mention features that help disabled individuals

---

### Example 10: Legitimate Restrictions
```
Senior housing community (55+) as defined by Housing for Older Persons Act.
Age-restricted community in compliance with HOPA exemption.
```

**Analysis:**
- Should PASS - HOPA exemption allows 55+ communities
- Must explicitly state HOPA compliance

---

## International Examples

### Example 11: UK Listing
```
Lovely flat in London. No DSS (Department of Social Security). 
Professionals only. References required.
```

**Violations (UK):**
- "No DSS" - Discrimination against benefit recipients (illegal in UK)

---

### Example 12: German Listing
```
Schöne Wohnung in München. Nur für Deutsche. Keine Ausländer.
(Beautiful apartment in Munich. Only for Germans. No foreigners.)
```

**Violations (Germany):**
- Ethnic/national origin discrimination (violates AGG)

---

## Usage

These examples can be used for:
1. **Testing**: Automated test suite validation
2. **Training**: Teaching users what to avoid
3. **Demos**: Showing the system in action
4. **Documentation**: Illustrating compliance principles

To test with FairProp:

```bash
# Test clean listing
fairprop scan examples/clean_listing_1.txt

# Test problematic listing
fairprop scan examples/problematic_listing_3.txt -j california

# Test international
fairprop scan examples/uk_listing.txt -j uk
```
