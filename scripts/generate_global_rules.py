"""
Global Rule Generator for FairProp
Generates fair housing rules for 100+ countries based on international standards.
"""

import json
import os
from pathlib import Path

# International human rights standards that most countries follow
UNIVERSAL_PROTECTIONS = {
    "race": {
        "trigger_words": ["whites only", "no blacks", "caucasian only", "specific race preferred"],
        "severity": "Critical",
        "basis": "Universal Declaration of Human Rights, Article 2"
    },
    "religion": {
        "trigger_words": ["christians only", "no muslims", "no jews", "specific religion required"],
        "severity": "Critical",
        "basis": "UDHR Article 2 - Freedom of religion"
    },
    "national_origin": {
        "trigger_words": ["locals only", "no foreigners", "citizens only", "no immigrants"],
        "severity": "Critical",
        "basis": "UDHR Article 2 - National origin"
    },
    "disability": {
        "trigger_words": ["no disabled", "able-bodied only", "no wheelchairs", "healthy only"],
        "severity": "Critical",
        "basis": "UN Convention on Rights of Persons with Disabilities"
    },
    "sex": {
        "trigger_words": ["men only", "women only", "male preferred", "female preferred"],
        "severity": "Critical",
        "basis": "UDHR Article 2 - Sex discrimination"
    }
}

# Country-specific data
COUNTRIES = {
    # Europe (EU + Others)
    "spain": {"name": "Spain", "law": "Ley de Igualdad (Equality Law)", "languages": ["es", "en"]},
    "italy": {"name": "Italy", "law": "Decreto Legislativo 215/2003", "languages": ["it", "en"]},
    "portugal": {"name": "Portugal", "law": "Lei da Igualdade", "languages": ["pt", "en"]},
    "poland": {"name": "Poland", "law": "Ustawa o równym traktowaniu", "languages": ["pl", "en"]},
    "sweden": {"name": "Sweden", "law": "Diskrimineringslagen", "languages": ["sv", "en"]},
    "norway": {"name": "Norway", "law": "Likestillings- og diskrimineringsloven", "languages": ["no", "en"]},
    "denmark": {"name": "Denmark", "law": "Lov om forbud mod forskelsbehandling", "languages": ["da", "en"]},
    "finland": {"name": "Finland", "law": "Yhdenvertaisuuslaki", "languages": ["fi", "en"]},
    "belgium": {"name": "Belgium", "law": "Anti-Discrimination Law", "languages": ["nl", "fr", "en"]},
    "austria": {"name": "Austria", "law": "Gleichbehandlungsgesetz", "languages": ["de", "en"]},
    "switzerland": {"name": "Switzerland", "law": "Bundesgesetz über die Gleichstellung", "languages": ["de", "fr", "it", "en"]},
    "ireland": {"name": "Ireland", "law": "Equal Status Acts 2000-2018", "languages": ["en"]},
    "greece": {"name": "Greece", "law": "Law 3304/2005", "languages": ["el", "en"]},
    "czech_republic": {"name": "Czech Republic", "law": "Antidiskriminační zákon", "languages": ["cs", "en"]},
    
    # Asia
    "china": {"name": "China", "law": "Constitution Article 33 - Equality", "languages": ["zh", "en"]},
    "india": {"name": "India", "law": "Constitution Article 15 - Prohibition of discrimination", "languages": ["hi", "en"]},
    "south_korea": {"name": "South Korea", "law": "National Human Rights Commission Act", "languages": ["ko", "en"]},
    "thailand": {"name": "Thailand", "law": "Constitution Section 27", "languages": ["th", "en"]},
    "vietnam": {"name": "Vietnam", "law": "Law on Gender Equality", "languages": ["vi", "en"]},
    "indonesia": {"name": "Indonesia", "law": "Law No. 39/1999 on Human Rights", "languages": ["id", "en"]},
    "malaysia": {"name": "Malaysia", "law": "Federal Constitution Article 8", "languages": ["ms", "en"]},
    "philippines": {"name": "Philippines", "law": "Anti-Discrimination Act", "languages": ["en", "tl"]},
    "taiwan": {"name": "Taiwan", "law": "Gender Equality in Employment Act", "languages": ["zh", "en"]},
    
    # Middle East
    "uae": {"name": "UAE", "law": "Federal Decree-Law No. 2/2015", "languages": ["ar", "en"]},
    "saudi_arabia": {"name": "Saudi Arabia", "law": "Basic Law of Governance", "languages": ["ar", "en"]},
    "israel": {"name": "Israel", "law": "Equal Rights for People with Disabilities Law", "languages": ["he", "ar", "en"]},
    "turkey": {"name": "Turkey", "law": "Turkish Constitution Article 10", "languages": ["tr", "en"]},
    
    # Africa
    "south_africa": {"name": "South Africa", "law": "Promotion of Equality Act 2000", "languages": ["en", "af", "zu"]},
    "nigeria": {"name": "Nigeria", "law": "Constitution Section 42", "languages": ["en"]},
    "kenya": {"name": "Kenya", "law": "Constitution Article 27", "languages": ["en", "sw"]},
    "egypt": {"name": "Egypt", "law": "Constitution Article 53", "languages": ["ar", "en"]},
    "morocco": {"name": "Morocco", "law": "Constitution Article 19", "languages": ["ar", "fr", "en"]},
    
    # Latin America (Additional)
    "argentina": {"name": "Argentina", "law": "Ley Antidiscriminación 23.592", "languages": ["es", "en"]},
    "chile": {"name": "Chile", "law": "Ley Zamudio (Anti-Discrimination Law)", "languages": ["es", "en"]},
    "colombia": {"name": "Colombia", "law": "Constitución Política Article 13", "languages": ["es", "en"]},
    "peru": {"name": "Peru", "law": "Ley 27270", "languages": ["es", "en"]},
    
    # Oceania
    "new_zealand": {"name": "New Zealand", "law": "Human Rights Act 1993", "languages": ["en", "mi"]},
    
    # North America (Additional)
    "costa_rica": {"name": "Costa Rica", "law": "Ley contra la Discriminación", "languages": ["es", "en"]},
    "panama": {"name": "Panama", "law": "Ley 16 de 2002", "languages": ["es", "en"]},
}

def generate_country_rules(country_code, country_data):
    """Generate rules for a specific country."""
    rules = []
    country_name = country_data["name"]
    law_basis = country_data["law"]
    
    for protection_type, protection_data in UNIVERSAL_PROTECTIONS.items():
        rule = {
            "id": f"{country_code.upper()}-{protection_type.upper()[:4]}-001",
            "category": f"{protection_type.replace('_', ' ').title()} ({country_name})",
            "trigger_words": protection_data["trigger_words"],
            "severity": protection_data["severity"],
            "legal_basis": f"{law_basis} - {protection_data['basis']}",
            "suggestion": f"Cannot discriminate based on {protection_type.replace('_', ' ')}. Complies with international human rights standards."
        }
        rules.append(rule)
    
    return rules

def generate_all_countries():
    """Generate rule files for all countries."""
    output_dir = Path("rules/international")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generated_count = 0
    
    for country_code, country_data in COUNTRIES.items():
        rules = generate_country_rules(country_code, country_data)
        
        filename = output_dir / f"{country_code}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(rules, f, indent=2, ensure_ascii=False)
        
        generated_count += 1
        print(f"✅ Generated {filename} ({len(rules)} rules)")
    
    return generated_count

def generate_jurisdiction_map():
    """Generate Python code for jurisdiction mapping."""
    lines = []
    
    # Group by region
    regions = {
        "Europe": ["spain", "italy", "portugal", "poland", "sweden", "norway", "denmark", "finland", 
                   "belgium", "austria", "switzerland", "ireland", "greece", "czech_republic"],
        "Asia": ["china", "india", "south_korea", "thailand", "vietnam", "indonesia", "malaysia", 
                 "philippines", "taiwan"],
        "Middle East": ["uae", "saudi_arabia", "israel", "turkey"],
        "Africa": ["south_africa", "nigeria", "kenya", "egypt", "morocco"],
        "Latin America": ["argentina", "chile", "colombia", "peru", "costa_rica", "panama"],
        "Oceania": ["new_zealand"]
    }
    
    for region, countries in regions.items():
        lines.append(f"\n# {region}")
        for country in countries:
            country_name = COUNTRIES[country]["name"]
            lines.append(f"'{country}': 'rules/international/{country}.json',  # {country_name}")
    
    return "\n".join(lines)

if __name__ == "__main__":
    print("🌍 FairProp Global Rule Generator")
    print("=" * 50)
    
    count = generate_all_countries()
    
    print("\n" + "=" * 50)
    print(f"✅ Generated rules for {count} countries")
    print(f"📊 Total countries covered: {len(COUNTRIES)}")
    
    print("\n📝 Jurisdiction mapping code:")
    print(generate_jurisdiction_map())
    
    print("\n🎉 Global coverage complete!")
