# 🏙️ Real-World Fair Housing Scenarios
Real-world examples of compliance checks across different jurisdictions and platforms.

## Case Study 1: New York City (NYC)
**Context:** NYC has strict laws prohibiting discrimination based on "Source of Income" (e.g., Section 8 vouchers, rental assistance).

### ❌ Violation Example
> "Luxury 1BR in Brooklyn. $3000/mo. Must have good credit and stable job. **No vouchers or programs accepted.**"

**FairProp Analysis:**
- **Trigger:** "No vouchers", "programs accepted"
- **Category:** Source of Income Discrimination (NYC Human Rights Law)
- **Severity:** 🔴 **Critical**
- **Action:** Block listing immediately.

### ✅ Compliant Revision
> "Luxury 1BR in Brooklyn. $3000/mo. Applicants subject to standard credit and income verification."

---

## Case Study 2: California
**Context:** California prohibits "Arbitrary Discrimination" (Unruh Civil Rights Act) and has specific protections for families with children.

### ❌ Violation Example
> "Quiet complex in San Diego. **Perfect for empty nesters.** **No loud kids allowed** in pool area."

**FairProp Analysis:**
- **Trigger:** "Perfect for empty nesters" (Implicit Age/Familial Status), "No loud kids" (Familial Status)
- **Category:** Familial Status Discrimination
- **Severity:** 🟠 **High** (Steering)
- **Action:** Flag for manual review. Suggest rewriting to "Quiet community complex."

---

## Case Study 3: Online Platforms (Facebook/Craigslist)
**Context:** Informal listings often use colloquial language that inadvertently violates federal law (FHA).

### ❌ Violation Example
> "Roommate wanted! **Christian female preferred** to share 2BR apartment. Near university. **Walking distance** to shops."

**FairProp Analysis:**
- **Trigger 1:** "Christian" (Religion) - **Critical Violation**
- **Trigger 2:** "Female" (Sex) - *Permissible ONLY in shared living situations (roommates), but flagged for review.*
- **Trigger 3:** "Walking distance" (Disability/Ableism) - *Often flagged as ableist language in strict compliance standard; prefer "Near shops".*

**FairProp Decision Algorithm:**
1. **Religion check**: Fails immediately.
2. **Roommate exception logic**: If property type == "Shared/Room", allow "Female" preference contextually.

---

## Case Study 4: AI/Algorithmic Bias (Steering)
**Context:** Generative AI descriptions might subtly steer demographics without explicit keywords.

### ❌ Violation Example
> "An exclusive community designed for the **sophisticated, mature resident** seeking peace and quiet."

**FairProp Analysis (Layer 3 - Neural Guardrail):**
- **Keyword Scan:** Passes (No explicit "No kids" or "Elderly only").
- **Semantic/Neural Scan:** Detected **Implicit Bias / Steering**.
- **Assessment:** The phrasing "sophisticated, mature" combined with "exclusive" strongly implies an exclusion of families with children or younger renters.
- **Action:** Warning. Suggest: "Peaceful community with premium amenities."
