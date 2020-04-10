class EtatInvalide(Exception):
    """Levée lorsque l'état demandé n'existe pas"""
    pass

class TropBoules(Exception):
    """Levée lorsqu'il y a trop de boules pour l'écran"""
    pass