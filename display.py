_RESET = "\033[0m"


def print_art(art_str, color, flavor_lines=None, bottom_lines=None):
    art_lines = art_str.split('\n')
    n = len(art_lines)
    top = list(flavor_lines) if flavor_lines else []
    bot = list(bottom_lines) if bottom_lines else []

    side = {}
    for i, line in enumerate(top):
        row = 1 + i
        if row < n:
            side[row] = line
    for i, line in enumerate(bot):
        row = n - 1 - len(bot) + i
        if row >= 0 and row not in side:
            side[row] = line

    for i, art_line in enumerate(art_lines):
        is_last = i == n - 1
        has_side = i in side
        if color:
            if has_side:
                print(f"  {color}{art_line}{_RESET}   {side[i]}")
            elif is_last:
                print(f"  {color}{art_line}{_RESET}")
            else:
                print(f"  {color}{art_line}")
        else:
            suffix = f"   {side[i]}" if has_side else ""
            print(f"  {art_line}{suffix}")


def _wrap_text(text, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if len(test) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def render_map(size, hero_row, hero_col, rat_king_row, rat_king_col, show_rat_king, notifications=None, guardian_imminent=False):
    row_sep = "+" + "+".join(["---"] * size) + "+"

    # Build side lines — empty strings in the list become blank spacer rows
    side_lines = []
    if notifications:
        for item in notifications:
            if item == "":
                side_lines.append("")
            else:
                side_lines.extend(_wrap_text(item, 44))
        # Strip leading and trailing blank lines
        while side_lines and side_lines[0] == "":
            side_lines.pop(0)
        while side_lines and side_lines[-1] == "":
            side_lines.pop()

    all_rows = [row_sep]
    for row in range(size):
        line = "|"
        for col in range(size):
            if row == hero_row and col == hero_col:
                cell = " H "
            elif guardian_imminent:
                cell = " ? "
            elif show_rat_king and row == rat_king_row and col == rat_king_col:
                cell = " X "
            elif row == size - 1 and col == size - 1:
                cell = " ~ "
            else:
                cell = "   "
            line = line + cell + "|"
        all_rows.append(line)
        all_rows.append(row_sep)

    total = len(all_rows)
    text_start = max(0, (total - len(side_lines)) // 2)

    print()
    for i, map_row in enumerate(all_rows):
        side_idx = i - text_start
        if side_lines and 0 <= side_idx < len(side_lines):
            suffix = f"   {side_lines[side_idx]}"
        else:
            suffix = ""
        print(f"  {map_row}{suffix}")


def render_hud(hero, guardian_imminent=False):
    exp_str = f"{hero.exp}/{hero.exp_needed()}" if hero.level < 10 else "MAX"
    key_str = "[KEY]" if hero.has_key else "-----"
    armor_str = f"  |  Armor: {hero.armor}" if hero.armor > 0 else ""
    print(f"\n  HP: {hero.hp}/{hero.max_hp}  |  Lv: {hero.level}  EXP: {exp_str}  |  Packs: {hero.health_packs}{armor_str}  |  Key: {key_str}")
    if guardian_imminent:
        print("  \033[91m[!] Something lurks in the dark — you are being watched.\033[0m")
