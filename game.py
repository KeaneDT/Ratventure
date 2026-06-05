import random
from entities import Hero, RatMinion, PlagueRat, StealthRat, RatGuardian, RatKing, FriendlyRat
from combat import run_combat
from display import render_map, render_hud, print_art

DEFAULT_SIZE = 7

DIRECTION_NAMES = {
    "W": "Up",
    "S": "Down",
    "A": "Left",
    "D": "Right"
}

RAT_KILL_FLAVOUR = {
    RatMinion: [
        "It claws the dirt: '...ten must fall...the Guardian wakes...'",
        "With its last breath: '...you cannot stop what is coming...'",
        "It hisses faintly: '...our numbers thin...soon he stirs...'",
        "'...the Guardian...will avenge us...'",
        "It scratches at the stone: '...more will come...always more...'",
        "A dying whisper: '...the King sees through our eyes...he sees you...'",
        "'...we are his army...there is no end to us...'",
        "It stills: '...you have earned...his attention...'",
    ],
    PlagueRat: [
        "Through rotting teeth: '...the plague feeds him...the Guardian grows stronger...'",
        "As it crumbles: '...sickness spreads...he feasts on it...'",
        "'...ten of us fall...and the Guardian...rises...'",
        "It dissolves slowly: '...the curse lives on...in every wound you carry...'",
        "'...I bore the King's sickness proudly...now so do you...'",
        "A wet gurgle: '...the Guardian smells your wounds...he is coming...'",
    ],
    StealthRat: [
        "The shadows whisper: '...the unseen one watches...he is almost here...'",
        "A fading voice: '...the Guardian moves through shadows...as we do...'",
        "'...when enough blood is spilled...he will emerge...'",
        "The darkness stills: '...you fought well...the Guardian will not make it easy...'",
        "'...we were the King's eyes...now you fight blind...'",
        "A final whisper from nowhere: '...he already knows where you are...'",
    ],
}

RAT_KILL_FLAVOUR_LATE = {
    RatMinion: [
        "It squeaks faintly: '...the Guardian is gone...we are lost...'",
        "'...the King grows desperate...find the key...'",
        "With its last twitch: '...fewer of us remain...but he still reigns...'",
        "It claws at nothing: '...the key is out there...somewhere...'",
        "'...the King trembles on his throne...but he will not run...'",
        "A last gasp: '...you will never find it in time...'",
    ],
    PlagueRat: [
        "Through crumbling flesh: '...even plague cannot save us now...'",
        "'...the curse weakens...but the King still breathes...'",
        "It dissolves: '...find the key if you can...the King will be ready...'",
        "'...we rot while the King feasts...some loyalty that is...'",
        "A bitter rattle: '...I should have deserted when I had the chance...'",
    ],
    StealthRat: [
        "The shadow dissolves: '...there is no hiding from you...'",
        "'...the King cowers in his keep...but he will not yield...'",
        "A faint echo: '...the key changes hands...it will find you...'",
        "'...I ran from the King once...he sent three of us to drag me back...'",
        "The darkness sighs: '...finish this...for all of us...'",
    ],
}


def ask_map_size():
    print("\n  ╔══════════════════════════════════════╗")
    print("  ║        WELCOME TO RATVENTURE         ║")
    print("  ╚══════════════════════════════════════╝")
    choice = input(f"\n  Use default {DEFAULT_SIZE}x{DEFAULT_SIZE} map? (y/n): ").strip().lower()
    if choice == "n":
        while True:
            size_input = input("  Enter map size (min 5): ").strip()
            if size_input.isdigit() and int(size_input) >= 5:
                return int(size_input)
            print("  Please enter a number of 5 or more.")
    return DEFAULT_SIZE


def get_valid_directions(row, col, size):
    directions = []
    if row > 0:
        directions.append("W")
    if row < size - 1:
        directions.append("S")
    if col > 0:
        directions.append("A")
    if col < size - 1:
        directions.append("D")
    return directions


_MOVE_DELTAS = {"W": (-1, 0), "S": (1, 0), "A": (0, -1), "D": (0, 1)}

def apply_direction(row, col, direction):
    dr, dc = _MOVE_DELTAS[direction]
    return row + dr, col + dc


def spawn_rat():
    if random.random() < 0.10:
        return FriendlyRat()
    level = random.randint(1, 5)
    roll = random.random()
    if roll < 0.60:
        return RatMinion(level)
    elif roll < 0.80:
        return PlagueRat(level)
    else:
        return StealthRat(level)


def _notify(notifications, *lines):
    if notifications:
        notifications.append("")
    for line in lines:
        notifications.append(line)


def handle_drops(hero, rat, map_size, guardian_defeated, notifications):
    if guardian_defeated and not hero.has_key:
        if random.random() < max(0.30, 1 / map_size):
            hero.has_key = True
            _notify(notifications,
                "The rat dropped a KEY!",
                "An ornate key engraved with a rat's skull.")

    if random.random() < rat.health_pack_drop_rate:
        hero.health_packs += 1
        _notify(notifications,
            f"You found a Health Pack! ({hero.health_packs} total)",
            "A bundle of herbs and cloth.")

    if hero.weapon is None:
        if random.random() < 0.20:
            hero.weapon = "rat_teeth"
            _notify(notifications,
                "You found Rat Teeth — equipped! (1.25x damage)",
                "Sharp and yellowed. Still warm.")


def show_victory(hero, rats_killed):
    print("\n" * 20, end="")
    print("  ╔══════════════════════════════════════╗")
    print("  ║       VICTORY — PEACE RESTORED!      ║")
    print("  ╚══════════════════════════════════════╝")
    print()
    print()
    print("  The Rat King crumbles from his throne,")
    print("  his crown rolling across the stone floor.")
    print("  A silence falls over the land — then birdsong.")
    print("  The curse is lifted. The kingdom breathes again.")
    print()
    print()
    print("  ── FINAL STATS ─────────────────────────")
    print()
    print(f"  Level reached  : {hero.level}")
    print(f"  Rats slain     : {rats_killed}")
    print(f"  HP remaining   : {hero.hp}/{hero.max_hp}")
    if hero.weapon:
        print("  Weapon         : Rat Teeth")
    if hero.armor > 0:
        print(f"  Armor          : +{hero.armor} reduction")
    print()
    print("  ────────────────────────────────────────")
    print()
    print()
    input("  Press Enter to continue...")


def show_game_over(hero, rats_killed):
    print("\n" * 20, end="")
    print("  ╔══════════════════════════════════════╗")
    print("  ║           YOU HAVE FALLEN            ║")
    print("  ╚══════════════════════════════════════╝")
    print()
    print()
    print("  You fall. The silence is absolute.")
    print("  The Rat King endures on his throne of bone.")
    print("  The curse holds fast. The land weeps.")
    print()
    print()
    print("  ── FINAL STATS ─────────────────────────")
    print()
    print(f"  Level reached  : {hero.level}")
    print(f"  Rats slain     : {rats_killed}")
    print(f"  HP remaining   : {max(0, hero.hp)}/{hero.max_hp}")
    if hero.weapon:
        print("  Weapon         : Rat Teeth")
    if hero.armor > 0:
        print(f"  Armor          : +{hero.armor} reduction")
    print()
    print("  ────────────────────────────────────────")
    print()
    print()
    input("  Press Enter to continue...")


def show_help(rats_killed, guardian_defeated, hero):
    print("\n" * 20, end="")
    print("  ╔══════════════════════════════════════╗")
    print("  ║           HERO'S JOURNAL             ║")
    print("  ╚══════════════════════════════════════╝")
    print()
    print()
    print("  The Rat King has seized the ancient fortress")
    print("  and cursed the land. Crops wither. Villages")
    print("  fall silent. Only you dare venture forth.")
    print()
    print()
    print("  ── YOUR CURRENT QUEST ──────────────────")

    if not guardian_defeated and rats_killed < 10:
        remaining = 10 - rats_killed
        print()
        print("  The Rat King's grip is sealed by dark magic.")
        print("  His power is bound through his minions —")
        print("  only bloodshed weakens the curse.")
        print()
        print(f"  Rats slain : {rats_killed} / 10")
        print(f"  Slay {remaining} more rat{'s' if remaining != 1 else ''} to draw out the Guardian.")

    elif not guardian_defeated:
        print()
        print("  The air grows heavy. Something ancient stirs.")
        print("  You have shed enough blood to catch the eye")
        print("  of the Rat Guardian — the King's enforcer.")
        print()
        print("  It lurks nearby. Wander these lands and face it.")
        print("  Defeat it to break the King's outer seal.")

    elif not hero.has_key:
        print()
        print("  The Guardian is slain. Its death-rattle echoed")
        print("  across the realm — the King's vault is now")
        print("  vulnerable. The key to his fortress was scattered")
        print("  among the surviving rats.")
        print()
        print("  Search these lands. Slay rats. Find the key.")
        print("  Without it, the castle gates will not open.")

    else:
        print()
        print("  You hold the key. The castle looms somewhere")
        print("  in the far reaches of the map — marked with X.")
        print()
        print("  The Rat King awaits on his throne of bones.")
        print("  End his reign. Lift the curse. Save the kingdom.")

    print()
    print("  ────────────────────────────────────────")
    print()
    print()
    input("  Press Enter to continue...")


_ORANGE = "\033[38;5;208m"

CHEST_ART = """\
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠉⠉⠉⠉⠉⠉⠉⠉⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣾⠀⣿⣿⡿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⢿⣿⣿⠀⢷⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢰⡏⠀⣿⣿⠀⣴⣶⣶⣶⣶⣶⣶⣶⣶⣦⠀⣿⣿⡀⢸⡆⠀⠀⠀⠀
⠀⠀⠀⠀⢸⡇⠀⣿⣿⣆⠘⠻⠇⢠⣤⣤⡄⠸⠟⠋⣠⣿⣿⡇⢸⡇⠀⠀⠀⠀
⠀⠀⠀⠀⢸⣇⠀⣿⣿⣿⣿⣶⣆⣈⣉⣉⣁⣰⣶⣿⣿⣿⣿⠃⢸⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠈⣿⣀⣉⣉⠉⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠉⣉⣉⣀⣿⠀⠀⠀⠀⠀
⠀⠀⢀⡴⠀⣉⣉⠉⠉⠉⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠉⠉⠉⣉⣉⠀⢦⡀⠀⠀
⠀⠀⠈⣀⠀⣿⣿⠀⣿⣿⠀⠛⠛⠉⠉⠉⠉⠛⠛⠀⣿⣿⠀⣿⣿⠀⣀⠁⠀⠀
⠀⠀⢸⡇⢀⣿⣿⠀⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⠀⣿⣿⡀⢸⡇⠀⠀
⠀⠀⢸⡇⢸⣿⠀⣤⡤⢤⣄⠘⠻⠿⠿⠿⠿⠟⠃⣠⡤⢤⣤⠀⣿⡇⢸⡇⠀⠀
⠀⠀⢠⡄⢸⣿⠀⠛⠃⠘⠋⢸⣶⣶⣆⣰⣶⣶⡇⠙⠃⠘⠛⠀⣿⡇⢠⡄⠀⠀
⠀⠀⢠⡄⠸⣿⣿⠀⠷⠞⠀⠛⠛⠿⠿⠿⠿⠛⠛⠀⠳⠾⠀⣿⣿⠇⢠⡄⠀⠀
⠀⠀⠘⠗⠀⣿⣿⠀⣶⣶⠀⣿⣷⣶⣶⣶⣶⣾⣿⠀⣶⣶⠀⣿⣿⠀⠺⠃⠀⠀
⠀⠀⠀⠀⠀⠉⠉⠀⠉⠉⠀⠉⠉⠉⠉⠉⠉⠉⠉⠀⠉⠉⠀⠉⠉⠀⠀⠀⠀⠀"""


def _chest_flavor(hero):
    lines = ["── INVENTORY ──", ""]
    if hero.weapon == "rat_teeth":
        lines += ["[✓] Rat Teeth", "    1.25x damage"]
    else:
        lines += ["[ ] No weapon", ""]
    lines.append("")
    if hero.armor > 0:
        lines += [f"[✓] Armor  +{hero.armor}", ""]
    else:
        lines += ["[ ] No armor", ""]
    p = hero.health_packs
    lines.append(f"{p}x Health Pack{'s' if p != 1 else ''}" if p > 0 else "No health packs")
    return lines


def show_items(hero):
    while True:
        print("\n" * 20)
        print("  ╔══════════════════════════════════════╗")
        print("  ║              BACKPACK                ║")
        print("  ╚══════════════════════════════════════╝")
        print_art(CHEST_ART, _ORANGE, _chest_flavor(hero))
        print()

        if hero.health_packs > 0:
            print("  ── ACTIONS ─────────────────────────────")
            print("  1. Use Health Pack")
            print()
        print("  0. Back")

        choice = input("\n  > ").strip()

        if choice == "1" and hero.health_packs > 0:
            healed = hero.use_health_pack()
            if healed == 0:
                print("  You are already at full HP.")
            else:
                print(f"  You recover {healed} HP. ({hero.health_packs} packs left)")
        elif choice == "0":
            break
        else:
            print("  Invalid option.")


def run_game():
    size = ask_map_size()

    hero = Hero()
    hero_row = size - 1
    hero_col = size - 1

    king_spots = list({(0, 0), (0, size - 1), (size - 1, 0), (0, size // 2), (size // 2, 0)})
    rat_king_row, rat_king_col = random.choice(king_spots)
    rat_king = RatKing()

    rats_killed = 0
    guardian_defeated = False
    spring_hp_mark = hero.max_hp
    spring_visited = False
    pending_notifications = []

    print(f"\n  A {size}x{size} map awaits. Find the key. Defeat the Rat King.\n")

    while True:
        print("\n" * 20)
        guardian_imminent = not guardian_defeated and rats_killed >= 10
        render_hud(hero, guardian_imminent)
        render_map(size, hero_row, hero_col, rat_king_row, rat_king_col, hero.has_key, pending_notifications, guardian_imminent)
        pending_notifications = []

        print("\n  1. Move")
        print("  2. Help")
        print("  3. Backpack")
        print("  0. Quit")

        action = input("\n  > ").strip()

        if action == "0":
            print("\n  Farewell, hero.\n")
            return

        elif action == "2":
            show_help(rats_killed, guardian_defeated, hero)

        elif action == "3":
            show_items(hero)

        elif action == "1":
            while True:
                print("\n" * 20)
                guardian_imminent = not guardian_defeated and rats_killed >= 10
                render_hud(hero, guardian_imminent)
                render_map(size, hero_row, hero_col, rat_king_row, rat_king_col, hero.has_key, pending_notifications, guardian_imminent)
                pending_notifications = []

                valid_dirs = get_valid_directions(hero_row, hero_col, size)

                parts = [f"{d}. {DIRECTION_NAMES[d]}" for d in ["W", "A", "S", "D"] if d in valid_dirs]
                print("\n  ── MOVE ────────────────────────────────")
                print("  " + "  |  ".join(parts))
                print()
                print("  0. Back")

                move_choice = input("\n  > ").strip().upper()

                if move_choice == "0":
                    break

                if move_choice not in valid_dirs:
                    print("  Invalid direction.")
                    continue

                prev_row, prev_col = hero_row, hero_col
                hero_row, hero_col = apply_direction(hero_row, hero_col, move_choice)

                # Boss fight
                if hero.has_key and hero_row == rat_king_row and hero_col == rat_king_col:
                    if hero.level < 6:
                        print("\n  You sense overwhelming power from within the castle.")
                        print(f"  You are Lv.{hero.level} — the Rat King is formidable. (Recommended: Lv.6+)")
                        confirm = input("  Press on? (y/n): ").strip().lower()
                        if confirm != "y":
                            hero_row, hero_col = prev_row, prev_col
                            continue
                    print("\n  The Rat King blocks your path!")
                    result = run_combat(hero, rat_king)
                    if result == "win":
                        show_victory(hero, rats_killed)
                        return
                    elif result == "dead":
                        show_game_over(hero, rats_killed)
                        return

                # Guardian guaranteed once 10 rats killed
                elif not guardian_defeated and rats_killed >= 10:
                    guardian = RatGuardian()
                    result = run_combat(hero, guardian)

                    if result == "dead":
                        show_game_over(hero, rats_killed)
                        return

                    if result == "win":
                        guardian_defeated = True
                        hero.armor = 3
                        _notify(pending_notifications,
                            "Rat Guardian defeated!",
                            "A crude iron plate falls from its body.",
                            "Armor equipped — damage reduced by 3.")
                        _notify(pending_notifications,
                            "The Guardian's hold is broken.",
                            "The key can now drop from rats!")
                        level_msgs = hero.gain_exp(guardian.exp_reward)
                        if level_msgs:
                            _notify(pending_notifications, *level_msgs)

                # Random encounter (1/3 chance, skipped on spring tile)
                elif not (hero_row == size - 1 and hero_col == size - 1) and random.random() < 1 / 3:
                    rat = spawn_rat()
                    if isinstance(rat, FriendlyRat):
                        print("\n  A small rat steps forward, paws raised in surrender.")
                    result = run_combat(hero, rat)

                    if result == "dead":
                        show_game_over(hero, rats_killed)
                        return

                    if result == "win":
                        if isinstance(rat, FriendlyRat):
                            hero.hp = 5
                            _notify(pending_notifications,
                                "The realm mourns your cruelty.",
                                "An unseen force reduces your HP to 5.")
                        else:
                            rats_killed += 1

                            handle_drops(hero, rat, size, guardian_defeated, pending_notifications)

                            level_msgs = hero.gain_exp(rat.exp_reward)
                            if level_msgs:
                                _notify(pending_notifications, *level_msgs)

                            if not guardian_defeated:
                                if rats_killed == 10:
                                    _notify(pending_notifications,
                                        "Something shifts in the air...",
                                        "A low rumble echoes across the map.")
                                elif type(rat) in RAT_KILL_FLAVOUR:
                                    _notify(pending_notifications,
                                        random.choice(RAT_KILL_FLAVOUR[type(rat)]))
                            elif type(rat) in RAT_KILL_FLAVOUR_LATE:
                                _notify(pending_notifications,
                                    random.choice(RAT_KILL_FLAVOUR_LATE[type(rat)]))

                # Healing spring at spawn tile
                if hero_row == size - 1 and hero_col == size - 1 and hero.hp < spring_hp_mark:
                    heal = max(1, hero.max_hp // 4)
                    healed = min(heal, hero.max_hp - hero.hp)
                    hero.hp = min(hero.hp + heal, hero.max_hp)
                    spring_hp_mark = hero.hp
                    if not spring_visited:
                        _notify(pending_notifications,
                            "~ Healing Spring ~",
                            f"The cool water restores {healed} HP.",
                            "Return only when wounded.")
                        spring_visited = True
                    else:
                        _notify(pending_notifications,
                            "~ Healing Spring ~",
                            f"The cool water restores {healed} HP.")

        else:
            print("  Enter 1, 2, 3, or 0.")
