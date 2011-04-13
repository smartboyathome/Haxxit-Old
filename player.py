import copy, programs as progs

class Programs():
    selection = False
    current = None
    active = []
    enemies = []
    programs = [('Hack', 2, 2), ('Slingshot', 2, 2)]
    
    def __init__(self, progs=None):
        if progs != None:
            programs += progs

    def gen(self, spawns, enemies):
        self.active = copy.deepcopy(spawns)
        for enemy in enemies:
            self.enemies.append(getattr(progs, enemy[0])(enemy[1], True))
