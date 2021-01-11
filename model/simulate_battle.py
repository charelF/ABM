from random import randrange


def roll_dice():
    return randrange(1, 7)


def attack(units):
    if units >= 3:
        cast = [roll_dice(), roll_dice(), roll_dice()]

    elif units == 2:
        cast = [roll_dice(), roll_dice()]

    elif units == 1:
        cast = [roll_dice()]

    return sorted(cast, reverse=True)


def defend(units):
    if units >= 2:
        cast = [roll_dice(), roll_dice()]
    else:
        cast = [roll_dice()]

    return sorted(cast, reverse=True)


def battle(attackers, defenders):

    while attackers > 0 and defenders > 0:
        the_attack = attack(attackers)
        the_defense = defend(defenders)

        while len(the_attack) > 0 and len(the_defense) > 0:
            if the_attack.pop(0) > the_defense.pop(0):
                defenders -= 1

            else:
                attackers -= 1

    if attackers > 0:
        return attackers
    else:
        return -defenders
