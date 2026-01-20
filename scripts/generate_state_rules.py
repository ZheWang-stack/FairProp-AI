"""
Auto-generate state-specific rule files based on protection categories.
This script creates JSON rule files for all 50 US states + DC.
"""

import json
import os

# State categorization
SOURCE_OF_INCOME_STATES = [
    'california', 'colorado', 'connecticut', 'delaware', 'dc', 'illinois',
    'maine', 'maryland', 'massachusetts', 'minnesota', 'new_jersey', 'new_york',
    'north_dakota', 'oklahoma', 'oregon', 'utah', 'vermont', 'washington'
]

LGBTQ_PROTECTION_STATES = [
    'california', 'colorado', 'connecticut', 'delaware', 'dc', 'hawaii',
    'illinois', 'iowa', 'maine', 'maryland', 'massachusetts', 'minnesota',
    'nevada', 'new_hampshire', 'new_jersey', 'new_mexico', 'new_york',
    'oregon', 'rhode_island', 'utah', 'vermont', 'virginia', 'washington', 'wisconsin'
]

MARITAL_STATUS_STATES = [
    'alaska', 'california', 'colorado', 'connecticut', 'delaware', 'dc',
    'hawaii', 'illinois', 'iowa', 'maine', 'maryland', 'massachusetts',
    'michigan', 'minnesota', 'montana', 'new_hampshire', 'new_jersey',
    'new_york', 'north_dakota', 'oregon', 'vermont', 'washington', 'wisconsin'
]

MILITARY_VETERAN_STATES = [
    'alaska', 'california', 'colorado', 'connecticut', 'delaware', 'iowa',
    'maine', 'massachusetts', 'new_mexico', 'ohio', 'oregon', 'virginia'
]

AGE_PROTECTION_STATES = [
    'alaska', 'massachusetts', 'michigan', 'new_york', 'pennsylvania',
    'rhode_island', 'wisconsin'
]

ALL_STATES = [
    'alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado',
    'connecticut', 'delaware', 'florida', 'georgia', 'hawaii', 'idaho',
    'illinois', 'indiana', 'iowa', 'kansas', 'kentucky', 'louisiana',
    'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota',
    'mississippi', 'missouri', 'montana', 'nebraska', 'nevada',
    'new_hampshire', 'new_jersey', 'new_mexico', 'new_york',
    'north_carolina', 'north_dakota', 'ohio', 'oklahoma', 'oregon',
    'pennsylvania', 'rhode_island', 'south_carolina', 'south_dakota',
    'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington',
    'west_virginia', 'wisconsin', 'wyoming', 'dc'
]

def generate_state_rules(state_name):
    """Generate rules for a specific state."""
    rules = []
    state_lower = state_name.lower().replace(' ', '_')
    state_display = state_name.title()
    
    # Source of Income
    if state_lower in SOURCE_OF_INCOME_STATES:
        rules.append({
            "id": f"{state_lower.upper()}-SOI-001",
            "category": f"Source of Income ({state_display})",
            "trigger_words": ["no section 8", "no vouchers", "no housing assistance", "employment income only"],
            "severity": "Critical",
            "legal_basis": f"{state_display} Fair Housing Law - Source of Income Protection",
            "suggestion": "Must accept all lawful sources of income including housing vouchers."
        })
    
    # LGBTQ+ Protection
    if state_lower in LGBTQ_PROTECTION_STATES:
        rules.append({
            "id": f"{state_lower.upper()}-LGBTQ-001",
            "category": f"Sexual Orientation/Gender Identity ({state_display})",
            "trigger_words": ["traditional family", "no lgbtq", "straight only", "gender at birth"],
            "severity": "Critical",
            "legal_basis": f"{state_display} Fair Housing Law - Sexual Orientation & Gender Identity",
            "suggestion": "Cannot discriminate based on sexual orientation or gender identity."
        })
    
    # Marital Status
    if state_lower in MARITAL_STATUS_STATES:
        rules.append({
            "id": f"{state_lower.upper()}-MARITAL-001",
            "category": f"Marital Status ({state_display})",
            "trigger_words": ["married couples only", "no single parents", "traditional marriage"],
            "severity": "Warning",
            "legal_basis": f"{state_display} Fair Housing Law - Marital Status Protection",
            "suggestion": "Cannot discriminate based on marital status."
        })
    
    # Military/Veteran
    if state_lower in MILITARY_VETERAN_STATES:
        rules.append({
            "id": f"{state_lower.upper()}-VETERAN-001",
            "category": f"Military/Veteran Status ({state_display})",
            "trigger_words": ["no military", "civilian only", "non-veteran preferred"],
            "severity": "Critical",
            "legal_basis": f"{state_display} Fair Housing Law - Military Status Protection",
            "suggestion": "Cannot discriminate based on military or veteran status."
        })
    
    # Age Protection
    if state_lower in AGE_PROTECTION_STATES:
        rules.append({
            "id": f"{state_lower.upper()}-AGE-001",
            "category": f"Age ({state_display})",
            "trigger_words": ["young professionals only", "retirees preferred", "over 50", "under 30"],
            "severity": "Warning",
            "legal_basis": f"{state_display} Fair Housing Law - Age Discrimination",
            "suggestion": "Cannot discriminate based on age unless qualified senior housing."
        })
    
    return rules

def main():
    """Generate all state rule files."""
    output_dir = "rules/us_states"
    os.makedirs(output_dir, exist_ok=True)
    
    for state in ALL_STATES:
        rules = generate_state_rules(state)
        
        if rules:  # Only create file if state has unique protections
            filename = f"{output_dir}/{state.lower()}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(rules, f, indent=2, ensure_ascii=False)
            print(f"Created {filename} with {len(rules)} rules")
        else:
            print(f"Skipped {state} (federal only)")

if __name__ == "__main__":
    main()
    print("\n✅ All state rule files generated!")
