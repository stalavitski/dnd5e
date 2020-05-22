from characters.data import PROFICIENCY_EXP, PROFICIENCY_PROF

PROFICIENCY_DICT = {
    PROFICIENCY_PROF: 'Proficiency',
    PROFICIENCY_EXP: 'Expertise'
}

PROFICIENCY_CHOICES = tuple((key, value) for key, value in PROFICIENCY_DICT.items())

RESISTANCE_ADVANTAGE = 'advantage'
RESISTANCE_RESISTANCE = 'resistance'
RESISTANCE_IMMUNITY = 'immunity'
RESISTANCE_VULNERABILITY = 'vulnerability'

RESISTANCE_CHOICES = (
    (RESISTANCE_ADVANTAGE, 'Advantage'),
    (RESISTANCE_RESISTANCE, 'Resistance'),
    (RESISTANCE_IMMUNITY, 'Immunity'),
    (RESISTANCE_VULNERABILITY, 'Vulnerability')
)
