from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json
import os

class ColorCategory(Enum):
    NEUTRAL = "neutral"
    WARM = "warm"
    COOL = "cool"
    ACCENT = "accent"
    PASTEL = "pastel"
    EARTH = "earth"
    JEWEL = "jewel"

class StyleLevel(Enum):
    CASUAL = (1, "casual")
    SMART_CASUAL = (2, "smart_casual")
    BUSINESS_CASUAL = (3, "business_casual")
    FORMAL = (4, "formal")
    STREETWEAR = (1, "streetwear")
    ATHLEISURE = (1, "athleisure")
    BOHEMIAN = (1, "bohemian")
    MINIMALIST = (2, "minimalist")

    def __init__(self, value, label):
        self._value_ = value
        self.label = label

    def __lt__(self, other):
        if isinstance(other, StyleLevel):
            return self.value < other.value
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, StyleLevel):
            return self.value <= other.value
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, StyleLevel):
            return self.value > other.value
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, StyleLevel):
            return self.value >= other.value
        return NotImplemented

    def __str__(self):
        return self.label

class PatternType(Enum):
    SOLID = "solid"
    STRIPED = "striped"
    CHECKED = "checked"
    PLAID = "plaid"
    FLORAL = "floral"
    GEOMETRIC = "geometric"
    ABSTRACT = "abstract"
    ANIMAL = "animal"

class Occasion(Enum):
    WORK = "work"
    CASUAL = "casual"
    FORMAL = "formal"
    SPORT = "sport"
    PARTY = "party"
    DATE = "date"
    TRAVEL = "travel"
    BEACH = "beach"

@dataclass
class Color:
    name: str
    category: ColorCategory
    hex_code: str
    complementary_colors: List[str]
    analogous_colors: List[str]

@dataclass
class Pattern:
    type: PatternType
    scale: str  # small, medium, large
    density: str  # sparse, medium, dense

# Expanded color palette with relationships
COLOR_PALETTE = {
    # Neutrals
    "white": Color("white", ColorCategory.NEUTRAL, "#FFFFFF", ["black", "navy"], ["beige", "light gray"]),
    "black": Color("black", ColorCategory.NEUTRAL, "#000000", ["white", "gold"], ["charcoal", "navy"]),
    "gray": Color("gray", ColorCategory.NEUTRAL, "#808080", ["burgundy", "teal"], ["light gray", "dark gray"]),
    "beige": Color("beige", ColorCategory.NEUTRAL, "#F5F5DC", ["navy", "burgundy"], ["cream", "tan"]),
    "navy": Color("navy", ColorCategory.NEUTRAL, "#000080", ["white", "gold"], ["royal blue", "dark blue"]),
    "khaki": Color("khaki", ColorCategory.NEUTRAL, "#C3B091", ["burgundy", "teal"], ["tan", "olive"]),
    
    # Warm colors
    "red": Color("red", ColorCategory.WARM, "#FF0000", ["green", "teal"], ["burgundy", "coral"]),
    "orange": Color("orange", ColorCategory.WARM, "#FFA500", ["blue", "navy"], ["coral", "amber"]),
    "yellow": Color("yellow", ColorCategory.WARM, "#FFFF00", ["purple", "navy"], ["gold", "amber"]),
    "brown": Color("brown", ColorCategory.WARM, "#A52A2A", ["teal", "mint"], ["tan", "burgundy"]),
    
    # Cool colors
    "blue": Color("blue", ColorCategory.COOL, "#0000FF", ["orange", "amber"], ["navy", "teal"]),
    "green": Color("green", ColorCategory.COOL, "#008000", ["red", "burgundy"], ["mint", "olive"]),
    "purple": Color("purple", ColorCategory.COOL, "#800080", ["yellow", "gold"], ["lavender", "plum"]),
    
    # Accent colors
    "pink": Color("pink", ColorCategory.ACCENT, "#FFC0CB", ["mint", "sage"], ["rose", "coral"]),
    "teal": Color("teal", ColorCategory.ACCENT, "#008080", ["coral", "amber"], ["mint", "navy"]),
    "burgundy": Color("burgundy", ColorCategory.ACCENT, "#800020", ["sage", "mint"], ["maroon", "wine"]),
    
    # Pastel colors
    "mint": Color("mint", ColorCategory.PASTEL, "#98FF98", ["lavender", "pink"], ["sage", "seafoam"]),
    "lavender": Color("lavender", ColorCategory.PASTEL, "#E6E6FA", ["sage", "mint"], ["lilac", "periwinkle"]),
    "coral": Color("coral", ColorCategory.PASTEL, "#FF7F50", ["teal", "mint"], ["peach", "salmon"]),
    
    # Earth tones
    "olive": Color("olive", ColorCategory.EARTH, "#808000", ["burgundy", "wine"], ["sage", "khaki"]),
    "sage": Color("sage", ColorCategory.EARTH, "#BCB88A", ["burgundy", "wine"], ["olive", "mint"]),
    "rust": Color("rust", ColorCategory.EARTH, "#B7410E", ["teal", "mint"], ["terracotta", "amber"]),
    
    # Jewel tones
    "emerald": Color("emerald", ColorCategory.JEWEL, "#50C878", ["ruby", "burgundy"], ["forest", "jade"]),
    "sapphire": Color("sapphire", ColorCategory.JEWEL, "#0F52BA", ["amber", "gold"], ["navy", "royal"]),
    "ruby": Color("ruby", ColorCategory.JEWEL, "#E0115F", ["emerald", "sage"], ["burgundy", "wine"])
}

# Enhanced color compatibility rules
COLOR_COMPATIBILITY = {
    ColorCategory.NEUTRAL: [ColorCategory.NEUTRAL, ColorCategory.WARM, ColorCategory.COOL, 
                          ColorCategory.ACCENT, ColorCategory.PASTEL, ColorCategory.EARTH, ColorCategory.JEWEL],
    ColorCategory.WARM: [ColorCategory.NEUTRAL, ColorCategory.WARM, ColorCategory.EARTH],
    ColorCategory.COOL: [ColorCategory.NEUTRAL, ColorCategory.COOL, ColorCategory.PASTEL],
    ColorCategory.ACCENT: [ColorCategory.NEUTRAL, ColorCategory.PASTEL],
    ColorCategory.PASTEL: [ColorCategory.NEUTRAL, ColorCategory.COOL, ColorCategory.ACCENT],
    ColorCategory.EARTH: [ColorCategory.NEUTRAL, ColorCategory.WARM, ColorCategory.ACCENT],
    ColorCategory.JEWEL: [ColorCategory.NEUTRAL, ColorCategory.ACCENT]
}

# Enhanced style compatibility rules
STYLE_COMPATIBILITY = {
    StyleLevel.CASUAL: [StyleLevel.CASUAL, StyleLevel.SMART_CASUAL, StyleLevel.ATHLEISURE],
    StyleLevel.SMART_CASUAL: [StyleLevel.CASUAL, StyleLevel.SMART_CASUAL, StyleLevel.BUSINESS_CASUAL, StyleLevel.MINIMALIST],
    StyleLevel.BUSINESS_CASUAL: [StyleLevel.SMART_CASUAL, StyleLevel.BUSINESS_CASUAL, StyleLevel.FORMAL, StyleLevel.MINIMALIST],
    StyleLevel.FORMAL: [StyleLevel.BUSINESS_CASUAL, StyleLevel.FORMAL],
    StyleLevel.STREETWEAR: [StyleLevel.CASUAL, StyleLevel.STREETWEAR, StyleLevel.ATHLEISURE],
    StyleLevel.ATHLEISURE: [StyleLevel.CASUAL, StyleLevel.STREETWEAR, StyleLevel.ATHLEISURE],
    StyleLevel.BOHEMIAN: [StyleLevel.CASUAL, StyleLevel.BOHEMIAN],
    StyleLevel.MINIMALIST: [StyleLevel.SMART_CASUAL, StyleLevel.BUSINESS_CASUAL, StyleLevel.MINIMALIST]
}

# Pattern compatibility rules
PATTERN_COMPATIBILITY = {
    PatternType.SOLID: [PatternType.SOLID, PatternType.STRIPED, PatternType.CHECKED, PatternType.PLAID, 
                       PatternType.FLORAL, PatternType.GEOMETRIC, PatternType.ABSTRACT, PatternType.ANIMAL],
    PatternType.STRIPED: [PatternType.SOLID, PatternType.CHECKED],
    PatternType.CHECKED: [PatternType.SOLID, PatternType.STRIPED],
    PatternType.PLAID: [PatternType.SOLID],
    PatternType.FLORAL: [PatternType.SOLID],
    PatternType.GEOMETRIC: [PatternType.SOLID],
    PatternType.ABSTRACT: [PatternType.SOLID],
    PatternType.ANIMAL: [PatternType.SOLID]
}

# Occasion-based style requirements
OCCASION_REQUIREMENTS = {
    Occasion.WORK: {
        "min_style_level": StyleLevel.BUSINESS_CASUAL,
        "max_style_level": StyleLevel.FORMAL,
        "pattern_restrictions": [PatternType.ANIMAL, PatternType.FLORAL],
        "color_restrictions": ["neon", "bright"]
    },
    Occasion.CASUAL: {
        "min_style_level": StyleLevel.CASUAL,
        "max_style_level": StyleLevel.SMART_CASUAL,
        "pattern_restrictions": [],
        "color_restrictions": []
    },
    Occasion.FORMAL: {
        "min_style_level": StyleLevel.FORMAL,
        "max_style_level": StyleLevel.FORMAL,
        "pattern_restrictions": [PatternType.FLORAL, PatternType.GEOMETRIC, PatternType.ABSTRACT, PatternType.ANIMAL],
        "color_restrictions": ["neon", "bright"]
    },
    Occasion.SPORT: {
        "min_style_level": StyleLevel.ATHLEISURE,
        "max_style_level": StyleLevel.ATHLEISURE,
        "pattern_restrictions": [],
        "color_restrictions": []
    },
    Occasion.PARTY: {
        "min_style_level": StyleLevel.SMART_CASUAL,
        "max_style_level": StyleLevel.FORMAL,
        "pattern_restrictions": [],
        "color_restrictions": []
    },
    Occasion.DATE: {
        "min_style_level": StyleLevel.SMART_CASUAL,
        "max_style_level": StyleLevel.FORMAL,
        "pattern_restrictions": [PatternType.ANIMAL],
        "color_restrictions": ["neon"]
    },
    Occasion.TRAVEL: {
        "min_style_level": StyleLevel.CASUAL,
        "max_style_level": StyleLevel.SMART_CASUAL,
        "pattern_restrictions": [],
        "color_restrictions": []
    },
    Occasion.BEACH: {
        "min_style_level": StyleLevel.CASUAL,
        "max_style_level": StyleLevel.CASUAL,
        "pattern_restrictions": [],
        "color_restrictions": []
    }
}

class UserPreferences:
    def __init__(self, username: str):
        self.username = username
        self.preferences_file = f"preferences_{username}.json"
        self.load_preferences()
    
    def load_preferences(self):
        if os.path.exists(self.preferences_file):
            with open(self.preferences_file, 'r') as f:
                self.preferences = json.load(f)
        else:
            self.preferences = {
                "favorite_colors": [],
                "favorite_styles": [],
                "favorite_patterns": [],
                "disliked_colors": [],
                "disliked_styles": [],
                "disliked_patterns": [],
                "outfit_history": [],
                "outfit_ratings": {}
            }
            self.save_preferences()
    
    def save_preferences(self):
        with open(self.preferences_file, 'w') as f:
            json.dump(self.preferences, f)
    
    def add_favorite_outfit(self, outfit: Dict, rating: float):
        outfit_id = hash(str(outfit))
        self.preferences["outfit_history"].append(outfit_id)
        self.preferences["outfit_ratings"][outfit_id] = rating
        self.save_preferences()
    
    def get_outfit_rating(self, outfit: Dict) -> float:
        outfit_id = hash(str(outfit))
        return self.preferences["outfit_ratings"].get(outfit_id, 0.5)
    
    def update_preferences(self, new_preferences: Dict):
        self.preferences.update(new_preferences)
        self.save_preferences()

def get_pattern_type(item_type: str, color: str) -> Pattern:
    """Determine the pattern type of a clothing item."""
    # This is a simplified version - in a real system, this would be more sophisticated
    if "striped" in item_type.lower():
        return Pattern(PatternType.STRIPED, "medium", "medium")
    elif "plaid" in item_type.lower():
        return Pattern(PatternType.PLAID, "large", "dense")
    elif "floral" in item_type.lower():
        return Pattern(PatternType.FLORAL, "medium", "medium")
    elif "check" in item_type.lower():
        return Pattern(PatternType.CHECKED, "medium", "medium")
    elif "animal" in item_type.lower():
        return Pattern(PatternType.ANIMAL, "large", "sparse")
    else:
        return Pattern(PatternType.SOLID, "small", "sparse")

def are_patterns_compatible(pattern1: Pattern, pattern2: Pattern) -> bool:
    """Check if two patterns are compatible."""
    return pattern2.type in PATTERN_COMPATIBILITY[pattern1.type]

def score_pattern_combination(items: List[Dict]) -> float:
    """Score a combination of patterns based on compatibility rules."""
    if not items:
        return 0.0
    
    patterns = [get_pattern_type(item['type'], item['color']) for item in items]
    
    # Calculate pattern compatibility score
    compatible_pairs = 0
    total_pairs = 0
    
    for i in range(len(patterns)):
        for j in range(i + 1, len(patterns)):
            if are_patterns_compatible(patterns[i], patterns[j]):
                compatible_pairs += 1
            total_pairs += 1
    
    if total_pairs > 0:
        return compatible_pairs / total_pairs
    return 0.0

def get_color_category(color_name: str) -> ColorCategory:
    """Get the color category for a given color name."""
    color = COLOR_PALETTE.get(color_name.lower())
    if color:
        return color.category
    return ColorCategory.NEUTRAL  # Default to neutral if color not found

def are_colors_compatible(color1: str, color2: str) -> bool:
    """Check if two colors are compatible based on their categories."""
    cat1 = get_color_category(color1)
    cat2 = get_color_category(color2)
    return cat2 in COLOR_COMPATIBILITY[cat1]

def score_color_combination(colors: List[str]) -> float:
    """Score a combination of colors based on fashion rules."""
    if not colors:
        return 0.0
    
    score = 0.0
    neutral_count = sum(1 for color in colors if get_color_category(color) == ColorCategory.NEUTRAL)
    
    # Base score for having neutrals
    score += min(neutral_count / len(colors), 0.5)
    
    # Check compatibility between all color pairs
    compatible_pairs = 0
    total_pairs = 0
    
    for i in range(len(colors)):
        for j in range(i + 1, len(colors)):
            if are_colors_compatible(colors[i], colors[j]):
                compatible_pairs += 1
            total_pairs += 1
    
    if total_pairs > 0:
        score += (compatible_pairs / total_pairs) * 0.5
    
    return score

def get_style_level(item_type: str) -> StyleLevel:
    """Determine the style level of a clothing item based on its type."""
    style_mapping = {
        # Casual items
        "t-shirt": StyleLevel.CASUAL,
        "tank top": StyleLevel.CASUAL,
        "sweatshirt": StyleLevel.CASUAL,
        "hoodie": StyleLevel.CASUAL,
        "jeans": StyleLevel.CASUAL,
        "sneakers": StyleLevel.CASUAL,
        
        # Smart casual items
        "polo shirt": StyleLevel.SMART_CASUAL,
        "chinos": StyleLevel.SMART_CASUAL,
        "loafers": StyleLevel.SMART_CASUAL,
        "blazer": StyleLevel.SMART_CASUAL,
        
        # Business casual items
        "dress shirt": StyleLevel.BUSINESS_CASUAL,
        "dress pants": StyleLevel.BUSINESS_CASUAL,
        "dress shoes": StyleLevel.BUSINESS_CASUAL,
        
        # Formal items
        "suit": StyleLevel.FORMAL,
        "tie": StyleLevel.FORMAL,
        "formal shoes": StyleLevel.FORMAL
    }
    
    return style_mapping.get(item_type.lower(), StyleLevel.CASUAL)

def are_styles_compatible(style1: StyleLevel, style2: StyleLevel) -> bool:
    """Check if two style levels are compatible."""
    return style2 in STYLE_COMPATIBILITY[style1]

def score_style_combination(items: List[Dict]) -> float:
    """Score a combination of clothing items based on style compatibility."""
    if not items:
        return 0.0
    
    style_levels = [get_style_level(item['type']) for item in items]
    
    # Calculate style compatibility score
    compatible_pairs = 0
    total_pairs = 0
    
    for i in range(len(style_levels)):
        for j in range(i + 1, len(style_levels)):
            if are_styles_compatible(style_levels[i], style_levels[j]):
                compatible_pairs += 1
            total_pairs += 1
    
    if total_pairs > 0:
        return compatible_pairs / total_pairs
    return 0.0

def score_outfit(outfit: Dict, occasion: Optional[Occasion] = None, 
                user_preferences: Optional[UserPreferences] = None) -> Tuple[float, float, float, float]:
    """Score an outfit based on color, style, pattern compatibility, and personal preferences."""
    items = list(outfit.values())
    
    # Basic compatibility scores
    colors = [item['color'] for item in items]
    color_score = score_color_combination(colors)
    style_score = score_style_combination(items)
    pattern_score = score_pattern_combination(items)
    
    # Personal preference score
    preference_score = 0.5  # Default neutral score
    if user_preferences:
        preference_score = user_preferences.get_outfit_rating(outfit)
    
    # Occasion-based adjustments
    if occasion:
        requirements = OCCASION_REQUIREMENTS[occasion]
        style_levels = [get_style_level(item['type']) for item in items]
        min_style_value = min(style.value for style in style_levels)
        max_style_value = max(style.value for style in style_levels)
        min_required_value = requirements["min_style_level"].value
        max_required_value = requirements["max_style_level"].value
        
        # Adjust scores based on occasion requirements
        if min_style_value < min_required_value or max_style_value > max_required_value:
            style_score *= 0.5
        
        # Check for restricted patterns
        for item in items:
            pattern = get_pattern_type(item['type'], item['color'])
            if pattern.type in requirements["pattern_restrictions"]:
                pattern_score *= 0.5
        
        # Check for restricted colors
        for color in colors:
            if any(restricted in color.lower() for restricted in requirements["color_restrictions"]):
                color_score *= 0.5
    
    return color_score, style_score, pattern_score, preference_score 