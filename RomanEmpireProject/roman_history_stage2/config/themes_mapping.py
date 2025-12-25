# config/themes_mapping.py
# Definition and mapping rules for 6 core themes
CORE_TERRAIN_THEMES = {
    "external_threat": {
        "name": "External Threat Intensity",
        "description": "Severity of military pressure and barbarian invasions",
        "source_themes": ["Military Overextension", "Barbarian Invasions"],
        "rating_direction": "negative"  # Higher rating means more severe problems
    },
    "internal_stability": {
        "name": "Internal Stability Level", 
        "description": "Political stability and leadership effectiveness",
        "source_themes": ["Political Corruption", "Crisis of Leadership"],
        "rating_direction": "negative"  # Higher rating means more severe problems
    },
    "economic_development": {
        "name": "Economic Development Level",
        "description": "Economic prosperity and fiscal health", 
        "source_themes": ["Economic Decline"],
        "rating_direction": "positive"  # Higher rating means better conditions
    },
    "socio_cultural_vitality": {
        "name": "Socio-Cultural Vitality",
        "description": "Social cohesion and cultural creativity",
        "source_themes": ["Social Decay", "Decline of Civic Responsibility", "Cultural Fragmentation"],
        "rating_direction": "positive"  # Higher rating means better conditions
    },
    "religious_influence": {
        "name": "Religious Influence Level", 
        "description": "Influence of religious belief transformations",
        "source_themes": ["Religious Transformation"],
        "rating_direction": "neutral"  # Rating indicates influence magnitude
    },
    "governance_efficiency": {
        "name": "Governance System Efficiency",
        "description": "Administrative management and governance efficiency",
        "source_themes": ["Administrative Inefficiency"],
        "rating_direction": "positive"  # Higher rating means better conditions
    }
}