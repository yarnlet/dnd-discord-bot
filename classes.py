import random
from enum import Enum

class DiceType(Enum):
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12
    D20 = 20

    def __str__(self):
        return f'd{self.value}'
    
    def roll(self):
        return random.randint(1, self.value)
    
    def types(self):
        return [str(dice) for dice in DiceType]
    
    def values(self):
        return [dice.value for dice in DiceType]
    
class CharacterSheet: # TODO basic, needs more work
    def __init__(self, name: str, race: str, char_class: str, level: int):
        self.name = name
        self.race = race
        self.char_class = char_class
        self.level = level
        self.abilities = {
            'Strength': 10,
            'Dexterity': 10,
            'Constitution': 10,
            'Intelligence': 10,
            'Wisdom': 10,
            'Charisma': 10
        }
        self.skills = {
            'Acrobatics': 0,
            'Animal Handling': 0,
            'Arcana': 0,
            'Athletics': 0,
            'Deception': 0,
            'History': 0,
            'Insight': 0,
            'Intimidation': 0,
            'Investigation': 0,
            'Medicine': 0,
            'Nature': 0,
            'Perception': 0,
            'Performance': 0,
            'Persuasion': 0,
            'Religion': 0,
            'Sleight of Hand': 0,
            'Stealth': 0,
            'Survival': 0
        }
        self.inventory = []

    def update_ability(self, ability_name, score):
        if ability_name in self.abilities:
            self.abilities[ability_name] = score
        else:
            print(f"Ability {ability_name} not found.")

    def update_skill(self, skill_name, modifier):
        if skill_name in self.skills:
            self.skills[skill_name] = modifier
        else:
            print(f"Skill {skill_name} not found.")

    def add_item_to_inventory(self, item):
        self.inventory.append(item)

    def __str__(self):
        return (f"Name: {self.name}\n"
                f"Class: {self.char_class}\n"
                f"Level: {self.level}\n"
                f"Abilities: {self.abilities}\n"
                f"Skills: {self.skills}\n"
                f"Inventory: {self.inventory}")
    
class Inventory:
    def __init__(self) -> None:
        pass
