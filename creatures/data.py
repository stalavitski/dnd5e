from characters.data import PROFICIENCY_EXP, PROFICIENCY_PROF

PROFICIENCY_DICT = {
    PROFICIENCY_PROF: 'Proficiency',
    PROFICIENCY_EXP: 'Expertise'
}

PROFICIENCY_CHOICES = tuple((key, value) for key, value in PROFICIENCY_DICT.items())
