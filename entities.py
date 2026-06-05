import random

EXP_THRESHOLDS = [15, 35, 65, 105, 160, 230, 320, 430, 560]


class Hero:
    def __init__(self):
        self.level = 1
        self.exp = 0
        self.hp = 20
        self.max_hp = 20
        self.armor = 0
        self.has_key = False
        self.weapon = None
        self.health_packs = 0

    def get_attack(self):
        base = random.randint(2 + self.level // 2, 5 + self.level)
        if self.weapon == "rat_teeth":
            base = int(base * 1.25)
        return base

    def exp_needed(self):
        if self.level >= 10:
            return None
        return EXP_THRESHOLDS[self.level - 1]

    def gain_exp(self, amount):
        if self.level >= 10:
            return []
        self.exp += amount
        messages = []
        while self.level < 10:
            needed = self.exp_needed()
            if self.exp < needed:
                break
            self.exp -= needed
            self.level += 1
            self.max_hp += 3
            heal = self.max_hp // 2
            self.hp = min(self.hp + heal, self.max_hp)
            messages.append(f"LEVEL UP! Now Lv.{self.level}")
            messages.append(f"Max HP +3, healed {heal} HP.")
        return messages

    def use_health_pack(self):
        if self.hp >= self.max_hp:
            return 0
        heal = random.randint(6, 10)
        healed = min(heal, self.max_hp - self.hp)
        self.hp = min(self.hp + heal, self.max_hp)
        self.health_packs -= 1
        return healed


class RatMinion:
    def __init__(self, level):
        self.name = f"Rat Minion (Lv.{level})"
        self.level = level
        self.hp = random.randint(4 + level * 2, 7 + level * 3)
        self.max_hp = self.hp
        self.exp_reward = level * 12
        self.poison_per_round = 0
        self.health_pack_drop_rate = 0.25
        self.art_color = None
        self.flavor_lines = [
            "A wiry grunt of",
            "the King's army.",
            "",
            "No tricks. Just",
            "teeth and spite.",
        ]
        self.can_flee = True
        self.battle_lines = [
            "'For the King! For the swarm!'",
            "'We are endless, you cannot stop us all!'",
            "'My brothers will avenge me!'",
            "'You'll regret setting foot in these lands!'",
            "'The King's will cannot be broken!'",
            "'I've driven off braver souls than you!'",
            "'The Guardian is coming, enjoy your time.'",
            "'Every rat you kill only makes the King angrier.'",
            "'Run now and I'll let you live. Probably.'",
            "'You fight well. It still won't matter.'",
        ]
        self.death_lines = [
            "'...tell my brothers I fought well...'",
            "'...the swarm...is endless...'",
            "'...you won this battle...not the war...'",
            "'...the King...will hear of this...'",
            "'...more will come...always more...'",
        ]

    def get_attack(self):
        return random.randint(1 + self.level // 3, 2 + self.level)

    def try_dodge(self):
        return False


class PlagueRat:
    def __init__(self, level):
        self.name = f"Plague Rat (Lv.{level})"
        self.level = level
        base_hp = random.randint(4 + level * 2, 7 + level * 3)
        self.hp = max(1, int(base_hp * 0.7))
        self.max_hp = self.hp
        self.exp_reward = level * 12
        self.poison_per_round = random.randint(1 + level // 4, 2 + level // 3)
        self.health_pack_drop_rate = 0.70
        self.art_color = "\033[92m"
        self.flavor_lines = [
            "A sickly green mist",
            "drifts from its fur.",
            "",
            f"Poisons for {self.poison_per_round} dmg",
            "each round.",
        ]
        self.can_flee = True
        self.battle_lines = [
            "'Can you feel the sickness already?'",
            "'My bite carries a thousand deaths.'",
            "'The plague is the King's gift to you!'",
            "'Every wound I give festers long after I'm gone.'",
            "'I haven't bathed since the curse began. Lucky you.'",
            "'The rot I carry is older than your kingdom.'",
            "'The King brews the plague in his own veins.'",
            "'You'll be rotting beside me before long.'",
            "'They call it disease. We call it heritage.'",
            "'The sickness doesn't end when I do.'",
        ]
        self.death_lines = [
            "'...the plague lives on...in your blood now...'",
            "'...you carry my gift whether you want it or not...'",
            "'...the rot...outlasts us all...'",
            "'...the King will feast on your suffering...'",
            "'...I die clean. You won't.'",
        ]

    def get_attack(self):
        return random.randint(2, 2 + self.level)

    def try_dodge(self):
        return False


class StealthRat:
    def __init__(self, level):
        self.name = f"Stealth Rat (Lv.{level})"
        self.level = level
        base_hp = random.randint(4 + level * 2, 7 + level * 3)
        self.hp = max(1, int(base_hp * 0.7))
        self.max_hp = self.hp
        self.exp_reward = level * 12
        self.poison_per_round = 0
        self.health_pack_drop_rate = 0.70
        self.art_color = "\033[90m"
        self.flavor_lines = [
            "A shadow detaches",
            "from the darkness.",
            "",
            "Strikes fast and",
            "vanishes from sight.",
        ]
        self.can_flee = True
        self.battle_lines = [
            "'You can't hit what you can't see.'",
            "'I was behind you a moment ago.'",
            "'The shadows are mine. You're just visiting.'",
            "'Blink and I'll be somewhere else entirely.'",
            "'You're swinging at old air.'",
            "'The King taught us to vanish. Watch.'",
            "'I've circled you three times already.'",
            "'Fast hands. Faster shadows.'",
            "'You fight like someone who expects to be seen.'",
            "'I'll be the last thing you almost notice.'",
        ]
        self.death_lines = [
            "'...even shadows...must fall eventually...'",
            "'...well struck...I didn't expect that...'",
            "'...the darkness...closes in...'",
            "'...I vanish...for the last time...'",
            "'...you have good instincts...for a dead man...'",
        ]

    def get_attack(self):
        return random.randint(1 + self.level // 2, 3 + self.level)

    def try_dodge(self):
        return random.random() < 1 / 3


class RatGuardian:
    def __init__(self):
        self.name = "Rat Guardian"
        self.hp = 30
        self.max_hp = 30
        self.exp_reward = 80
        self.poison_per_round = 0
        self.health_pack_drop_rate = 0
        self.art_color = "\033[91m"
        self.flavor_lines = [
            "The King's enforcer.",
            "",
            "Scarred and massive,",
            "it blocks your path.",
        ]
        self.can_flee = False
        self.heal_chance = 1 / 3
        self.heal_range = (3, 6)
        self.battle_lines = [
            "'The King's will is absolute. As am I.'",
            "'None have passed through me and lived.'",
            "'I am the last wall between you and your grave.'",
            "'You bled ten rats dry for this. Was it worth it?'",
            "'The King doesn't need me to win. He sends me to be sure.'",
            "'I've crushed knights in fuller armor than yours.'",
            "'Your courage is noted. It won't save you.'",
            "'Every scar on my hide is from someone better than you.'",
            "'I take no pleasure in this. But I am very good at it.'",
            "'Fight harder. I want this to be worth my time.'",
        ]
        self.death_lines = [
            "'...impossible...no one has ever...'",
            "'...the King...is not...what you think he is...'",
            "'...I was his best...and you broke me...'",
            "'...tell no one of this...'",
            "'...the seal is broken...go then...finish it...'",
        ]

    def get_attack(self):
        return random.randint(4, 8)

    def try_dodge(self):
        return False


class RatKing:
    def __init__(self):
        self.name = "The Rat King"
        self.hp = 48
        self.max_hp = 48
        self.poison_per_round = 2
        self.art_color = "\033[93m"
        self.flavor_lines = [
            "He sits upon a throne",
            "of bone and ruin.",
            "",
            "End his reign.",
        ]
        self.can_flee = False
        self.heal_chance = 1 / 3
        self.heal_range = (5, 9)
        self.battle_lines = [
            "'Did you really think a key could unseat a king?'",
            "'I have ruled these bones for a thousand seasons.'",
            "'Your kingdom sent one hero. How deeply insulting.'",
            "'Every rat you slew died whispering your name to me.'",
            "'I built this throne from the bones of better men.'",
            "'You cannot kill what the darkness already owns.'",
            "'My curse runs deeper than your blade can reach.'",
            "'Look at you. Brave. Tired. Almost broken. Almost.'",
            "'This is where legends end, in a hall of old bones.'",
            "'I will give you one final chance to kneel.'",
        ]
        self.death_lines = [
            "'...impossible...a king does not fall to...'",
            "'...the curse...will outlast...my body...'",
            "'...I was eternal...what are you...?'",
            "'...it matters not...another will rise...'",
            "'...well played...hero...well played...'",
        ]

    def get_attack(self):
        return random.randint(5, 11)

    def try_dodge(self):
        return False


class FriendlyRat:
    def __init__(self):
        self.name = "Friendly Rat"
        self.hp = 10
        self.max_hp = 10
        self.exp_reward = 0
        self.poison_per_round = 0
        self.health_pack_drop_rate = 0
        self.art_color = "\033[94m"
        self.flavor_lines = [
            "A trembling rat,",
            "paws raised in peace.",
            "",
            "Passive. Will not",
            "fight back.",
        ]
        self.can_flee = True
        self.passive = True
        self.battle_lines = [
            "'Please, I don't want to fight you!'",
            "'I hate the King as much as you do!'",
            "'He drives us to battle against our will!'",
            "'I have a family, a litter, in the lower warrens!'",
            "'Spare me and I'll spread word of your mercy!'",
            "'The King is a tyrant. I deserted his army!'",
            "'I threw down my weapon. I am no threat to you!'",
            "'There are others like me, rats who want peace!'",
            "'Kill me and you become what you came here to fight.'",
            "'I beg you, there is still kindness left in this world!'",
        ]
        self.death_lines = [
            "'...I only wanted...to go home...'",
            "'...tell the others...there was a hero here once...'",
            "'...I forgive you...but the realm...will not...'",
        ]

    def get_attack(self):
        return 0

    def try_dodge(self):
        return False
