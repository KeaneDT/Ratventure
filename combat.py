import random
from display import print_art

RAT_ART = """\
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣶⣶⣦⡴⢶⣶⣶⣆⠸⠿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⣻⣿⣷⣾⣿⣿⡿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣤⠄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣾⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⣿⣿⣿⣿⠿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣟⠛⠻⣿⣿⣿⣿⣦⡈⠉⠛⠻⡆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣦⡈⢻⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣧⠈⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣀⡀⠸⣿⣿⣿⣿⣟⣀⣉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣾⡿⠟⠛⠀⠉⠛⠛⠛⠛⠛⠛⠛⠛⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢿⣧⣀⠀⠀⠀⠀⢀⣀⣠⣤⠶⠶⠶⠶⢶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠉⠛⠛⠛⠛⠉⠉⠀⠀⠀⠀⠀⣀⡼⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""


def apply_damage(hero, raw_damage):
    actual = max(1, raw_damage - hero.armor)
    hero.hp -= actual
    return actual


def print_damage(enemy_name, raw_damage, actual_damage, armor):
    if armor > 0 and actual_damage < raw_damage:
        blocked = raw_damage - actual_damage
        print(f"  {enemy_name} hits you for {actual_damage} damage. ({blocked} blocked by armor)")
    else:
        print(f"  {enemy_name} hits you for {actual_damage} damage.")


def _try_enemy_heal(enemy):
    if getattr(enemy, 'heal_chance', 0) and random.random() < enemy.heal_chance:
        gain = random.randint(*enemy.heal_range)
        gain = min(gain, enemy.max_hp - enemy.hp)
        if gain > 0:
            enemy.hp += gain
            print(f"  {enemy.name} regenerates {gain} HP!")


def run_combat(hero, enemy):
    can_flee = getattr(enemy, 'can_flee', True)
    pack_option = "3" if can_flee else "2"

    while True:
        print("\n" * 20)
        print(f"  ╔══════════════════════════════════════╗")
        print(f"  ║{enemy.name.upper():^38}║")
        print(f"  ╚══════════════════════════════════════╝")
        bottom = [random.choice(enemy.battle_lines)] if enemy.battle_lines else []
        print_art(RAT_ART, enemy.art_color, enemy.flavor_lines, bottom_lines=bottom)
        print(f"  Hero HP  : {hero.hp}/{hero.max_hp}")
        print(f"  Enemy HP : {enemy.hp}/{enemy.max_hp}")
        print("\n  ── ACTIONS ─────────────────────────────")
        action_parts = ["1. Attack"]
        if can_flee:
            action_parts.append("2. Flee (50%)")
        if hero.health_packs > 0:
            action_parts.append(f"{pack_option}. Use Health Pack ({hero.health_packs} remaining)")
        print("  " + "  |  ".join(action_parts))

        choice = input("\n  > ").strip()

        if choice == "1":
            if enemy.try_dodge():
                print(f"\n  The {enemy.name} vanishes — your attack misses!")
            else:
                damage = hero.get_attack()
                enemy.hp -= damage
                print(f"\n  You hit the {enemy.name} for {damage} damage.")

            if enemy.hp <= 0:
                print("\n" * 20)
                print(f"  ╔══════════════════════════════════════╗")
                print(f"  ║{enemy.name.upper():^38}║")
                print(f"  ╚══════════════════════════════════════╝")
                death_bottom = [random.choice(enemy.death_lines)] if enemy.death_lines else []
                print_art(RAT_ART, enemy.art_color, enemy.flavor_lines, bottom_lines=death_bottom)
                print(f"  Hero HP  : {hero.hp}/{hero.max_hp}")
                print(f"  Enemy HP : 0/{enemy.max_hp}")
                print("\n  ── ACTIONS ─────────────────────────────")
                input("  Press Enter to continue...\n  .\n  .")
                return "win"

            if not getattr(enemy, 'passive', False):
                raw = enemy.get_attack()
                actual = apply_damage(hero, raw)
                print_damage(enemy.name, raw, actual, hero.armor)

                if enemy.poison_per_round > 0:
                    hero.hp -= enemy.poison_per_round
                    print(f"  Poison seeps in — {enemy.poison_per_round} damage!")

                if hero.hp <= 0:
                    return "dead"

                _try_enemy_heal(enemy)

        elif choice == "2" and can_flee:
            if getattr(enemy, 'passive', False):
                print(f"\n  The {enemy.name} watches you go, relieved.")
                return "flee"

            if random.random() < 0.5:
                raw = enemy.get_attack()
                actual = apply_damage(hero, raw)
                print(f"\n  You escape — but {enemy.name} lands a parting blow!")
                print_damage(enemy.name, raw, actual, hero.armor)
                if enemy.poison_per_round > 0:
                    hero.hp -= enemy.poison_per_round
                    print(f"  Poison seeps in — {enemy.poison_per_round} damage!")
                if hero.hp <= 0:
                    return "dead"
                return "flee"

            raw = enemy.get_attack()
            actual = apply_damage(hero, raw)
            print(f"\n  Failed to flee!")
            print_damage(enemy.name, raw, actual, hero.armor)

            if enemy.poison_per_round > 0:
                hero.hp -= enemy.poison_per_round
                print(f"  Poison seeps in — {enemy.poison_per_round} damage!")

            if hero.hp <= 0:
                return "dead"

            _try_enemy_heal(enemy)

        elif choice == pack_option and hero.health_packs > 0:
            healed = hero.use_health_pack()
            if healed == 0:
                print("  You are already at full HP.")
            else:
                print(f"\n  You use a Health Pack and recover {healed} HP. ({hero.health_packs} left)")
                if not getattr(enemy, 'passive', False):
                    raw = enemy.get_attack()
                    actual = apply_damage(hero, raw)
                    print_damage(enemy.name, raw, actual, hero.armor)
                    if enemy.poison_per_round > 0:
                        hero.hp -= enemy.poison_per_round
                        print(f"  Poison seeps in — {enemy.poison_per_round} damage!")
                    if hero.hp <= 0:
                        return "dead"
                    _try_enemy_heal(enemy)

        else:
            if can_flee and hero.health_packs > 0:
                print("  Enter 1, 2, or 3.")
            elif can_flee or hero.health_packs > 0:
                print("  Enter 1 or 2.")
            else:
                print("  Enter 1.")
