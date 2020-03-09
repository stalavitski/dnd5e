ABILITY_STRENGTH = 'str'
ABILITY_DEXTERITY = 'dex'
ABILITY_CONSTITUTION = 'con'
ABILITY_INTELLIGENCE = 'int'
ABILITY_WISDOM = 'wis'
ABILITY_CHARISMA = 'cha'

ABILITY_DICT = {
    ABILITY_STRENGTH: 'Strength',
    ABILITY_DEXTERITY: 'Dexterity',
    ABILITY_CONSTITUTION: 'Constitution',
    ABILITY_INTELLIGENCE: 'Intelligence',
    ABILITY_WISDOM: 'Wisdom',
    ABILITY_CHARISMA: 'Charisma'
}

ABILITY_CHOICES = tuple((key, value) for key, value in ABILITY_DICT.items())
